"""
Rotas da interface web do SGC-TI.

Cada rota só faz três coisas: lê o formulário, chama o service da
funcionalidade e mostra o resultado. As permissões e validações são
das próprias classes de serviço; quando elas lançam NegocioException
(ou uma subclasse), a mensagem aparece na tela como alerta vermelho.

Modo demonstração: liga botões que normalmente ficariam escondidos
para o perfil logado (ex.: "Assumir" para um solicitante), para mostrar
na apresentação os cenários de exceção do Gherkin acontecendo.
"""
from functools import wraps

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for,
)

from helpdesk.domain.exceptions import NegocioException
from helpdesk.domain.models import Perfil, StatusChamado

bp = Blueprint("web", __name__)


# ---------------------------------------------------------------- helpers
def sv():
    return current_app.extensions["sgc"]


def usuario_atual():
    user_id = session.get("user_id")
    return sv().usuario_repo.buscar_por_id(user_id) if user_id else None


def modo_demo() -> bool:
    return bool(session.get("demo"))


def login_obrigatorio(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if usuario_atual() is None:
            session.pop("user_id", None)
            flash("Faça login para continuar.", "erro")
            return redirect(url_for("web.login"))
        return view(*args, **kwargs)
    return wrapper


def area_admin(view):
    """Telas de administração: abertas ao ADMIN ou a qualquer um no modo demonstração
    (aí quem bloqueia é o service, e a mensagem de erro aparece na tela)."""
    @wraps(view)
    @login_obrigatorio
    def wrapper(*args, **kwargs):
        if usuario_atual().perfil != Perfil.ADMIN and not modo_demo():
            flash("Acesso negado: permissão de administrador necessária", "erro")
            return redirect(url_for("web.chamados"))
        return view(*args, **kwargs)
    return wrapper


def executar(acao, mensagem_sucesso=None):
    """Executa a ação do service e transforma o resultado em alerta na tela."""
    try:
        retorno = acao()
    except NegocioException as erro:
        flash(str(erro), "erro")
        return False
    texto = mensagem_sucesso or (retorno if isinstance(retorno, str) else None)
    if texto:
        flash(texto, "sucesso")
    return True


def voltar(padrao="web.chamados"):
    return redirect(request.referrer or url_for(padrao))


@bp.app_context_processor
def variaveis_globais():
    return {
        "usuario": usuario_atual(),
        "demo": modo_demo(),
        "Perfil": Perfil,
        "StatusChamado": StatusChamado,
    }


@bp.app_template_filter("status_label")
def status_label(status):
    return {
        StatusChamado.ABERTO: "Aberto",
        StatusChamado.EM_ATENDIMENTO: "Em atendimento",
        StatusChamado.RESOLVIDO: "Resolvido",
    }.get(status, str(status))


# ------------------------------------------------------- F01 / F02: acesso
@bp.route("/")
def inicio():
    return redirect(url_for("web.chamados" if usuario_atual() else "web.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        try:
            usuario = sv().autenticacao.autenticar(email, request.form.get("senha", ""))
        except NegocioException as erro:
            flash(str(erro), "erro")
            return render_template("login.html", email=email)
        session["user_id"] = usuario.id
        flash(f"Bem-vindo(a), {usuario.nome}!", "sucesso")
        return redirect(url_for("web.chamados"))
    return render_template("login.html", email="")


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = {"nome": "", "email": ""}
    if request.method == "POST":
        form = {"nome": request.form.get("nome", ""), "email": request.form.get("email", "")}
        ok = executar(
            lambda: sv().autenticacao.cadastrar(form["nome"], form["email"],
                                                request.form.get("senha", "")),
            "Usuário cadastrado com sucesso como SOLICITANTE. Faça login.",
        )
        if ok:
            return redirect(url_for("web.login"))
    return render_template("cadastro.html", form=form)


@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("web.login"))


@bp.route("/demo", methods=["POST"])
def alternar_demo():
    session["demo"] = not modo_demo()
    flash("Modo demonstração " + ("ligado" if session["demo"] else "desligado") + ".", "info")
    return voltar()


# ------------------------------------------- F06 / F07 / F08 / F09: chamados
@bp.route("/chamados")
@login_obrigatorio
def chamados():
    usuario = usuario_atual()
    filtros = {
        "status": request.args.get("status", ""),
        "categoria": request.args.get("categoria", ""),
        "termo": request.args.get("termo", ""),
    }
    base = {
        "status": StatusChamado(filtros["status"]) if filtros["status"] else None,
        "categoria": filtros["categoria"] or None,
        "termo": filtros["termo"] or None,
    }
    consulta = sv().chamado_consulta

    # F09 - cada perfil vê os chamados conforme seu nível de acesso
    if usuario.perfil == Perfil.ADMIN:
        titulo_lista = "Todos os chamados do sistema"
        lista = consulta.filtrar_chamados(**base)
    elif usuario.perfil == Perfil.TECNICO:
        titulo_lista = "Chamados atribuídos a mim"
        lista = consulta.filtrar_chamados(responsavel_id=usuario.id, **base)
    else:
        titulo_lista = "Meus chamados"
        lista = consulta.filtrar_chamados(solicitante_id=usuario.id, **base)

    # Fila de chamados abertos sem responsável (para o técnico assumir - F07)
    mostrar_fila = usuario.perfil == Perfil.TECNICO or modo_demo()
    fila = [c for c in consulta.filtrar_chamados(status=StatusChamado.ABERTO)
            if c.responsavel is None] if mostrar_fila else []

    # F08 - no modo demonstração, qualquer usuário aparece na lista (para mostrar o erro)
    candidatos = [u for u in sv().usuario_repo.listar_todos()
                  if modo_demo() or u.perfil == Perfil.TECNICO]

    return render_template(
        "chamados.html",
        titulo_lista=titulo_lista, lista=lista, fila=fila, mostrar_fila=mostrar_fila,
        filtros=filtros, categorias=sv().categoria.listar_categorias(),
        candidatos=sorted(candidatos, key=lambda u: u.nome),
    )


@bp.route("/chamados/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_chamado():
    form = {"titulo": "", "descricao": "", "categoria": ""}
    if request.method == "POST":
        form = {k: request.form.get(k, "") for k in form}
        ok = executar(
            lambda: sv().chamado_criacao.abrir_chamado(
                usuario_atual(), form["titulo"], form["descricao"], form["categoria"]),
            "Chamado aberto com sucesso (status inicial: ABERTO).",
        )
        if ok:
            return redirect(url_for("web.chamados"))
    return render_template("novo_chamado.html", form=form,
                           categorias=sv().categoria.listar_categorias())


@bp.route("/chamados/<chamado_id>/assumir", methods=["POST"])
@login_obrigatorio
def assumir(chamado_id):
    executar(lambda: sv().chamado_operacao.assumir_chamado(usuario_atual(), chamado_id),
             "Chamado assumido. Status alterado para EM ATENDIMENTO.")
    return voltar()


@bp.route("/chamados/<chamado_id>/delegar", methods=["POST"])
@login_obrigatorio
def delegar(chamado_id):
    tecnico = sv().usuario_repo.buscar_por_id(request.form.get("tecnico_id", ""))
    nome = tecnico.nome if tecnico else ""
    executar(lambda: sv().chamado_operacao.delegar_chamado(usuario_atual(), chamado_id, tecnico),
             f"Chamado delegado para {nome}. Status alterado para EM ATENDIMENTO.")
    return voltar()


# ------------------------------------------- F03 / F04 / F05: administração
@bp.route("/admin/usuarios")
@area_admin
def usuarios():
    lista = sorted(sv().usuario_repo.listar_todos(), key=lambda u: u.nome)
    return render_template("usuarios.html", lista=lista)


@bp.route("/admin/usuarios/<usuario_id>/perfil", methods=["POST"])
@login_obrigatorio
def alterar_perfil(usuario_id):
    try:
        novo = Perfil(request.form.get("perfil", ""))
    except ValueError:
        flash("Perfil inválido", "erro")
        return voltar("web.usuarios")
    executar(lambda: sv().perfil.alterar_perfil(usuario_atual(), usuario_id, novo))
    return voltar("web.usuarios")


@bp.route("/admin/usuarios/<usuario_id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_usuario(usuario_id):
    executar(lambda: sv().usuario_gestao.excluir_usuario(usuario_atual(), usuario_id))
    if usuario_atual() is None:  # o usuário excluiu a própria conta
        session.pop("user_id", None)
        return redirect(url_for("web.login"))
    return voltar("web.usuarios")


@bp.route("/admin/perfis", methods=["GET", "POST"])
@area_admin
def perfis():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        executar(lambda: sv().perfil.cadastrar_tipo_usuario(
            usuario_atual(), nome, request.form.get("descricao", "")),
            f"Tipo de usuário \"{nome.strip().upper()}\" cadastrado com sucesso.")
        return redirect(url_for("web.perfis"))
    return render_template("perfis.html", tipos=sv().perfil._tipos)


# ------------------------------------------------- F10 / F11: categorias
@bp.route("/admin/categorias", methods=["GET", "POST"])
@area_admin
def categorias():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        executar(lambda: sv().categoria.cadastrar_categoria(
            usuario_atual(), nome, request.form.get("descricao", "")),
            f"Categoria \"{nome.strip()}\" cadastrada com sucesso.")
        return redirect(url_for("web.categorias"))

    chamados = sv().chamado_repo.listar_todos()
    lista = [(c, sum(1 for ch in chamados if ch.categoria and ch.categoria.id == c.id))
             for c in sv().categoria.listar_categorias()]
    return render_template("categorias.html", lista=lista)


@bp.route("/admin/categorias/<categoria_id>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_categoria(categoria_id):
    executar(lambda: sv().categoria.remover_categoria(usuario_atual(), categoria_id))
    return voltar("web.categorias")
