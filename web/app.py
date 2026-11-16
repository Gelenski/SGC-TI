import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for caminho in (RAIZ, RAIZ / "src"):
    if str(caminho) not in sys.path:
        sys.path.insert(0, str(caminho))

from flask import Flask

from helpdesk.repositories import (
    UsuarioRepositoryEmMemoria,
    CategoriaRepositoryEmMemoria,
    ChamadoRepositoryEmMemoria,
)
from helpdesk.services import (
    AutenticacaoService,
    PerfilService,
    UsuarioGestaoService,
    ChamadoCriacaoService,
    ChamadoOperacaoService,
    CategoriaService,
    ChamadoConsultaService,
)
from web.seed import carregar_dados_de_exemplo


class Servicos:

    def __init__(self):
        self.usuario_repo = UsuarioRepositoryEmMemoria()
        self.categoria_repo = CategoriaRepositoryEmMemoria()
        self.chamado_repo = ChamadoRepositoryEmMemoria()

        self.autenticacao = AutenticacaoService(self.usuario_repo)
        self.perfil = PerfilService(self.usuario_repo)
        self.usuario_gestao = UsuarioGestaoService(self.usuario_repo)
        self.chamado_criacao = ChamadoCriacaoService(self.chamado_repo,
                                                     self.categoria_repo)
        self.chamado_operacao = ChamadoOperacaoService(self.chamado_repo)
        self.chamado_consulta = ChamadoConsultaService(self.chamado_repo)
        self.categoria = CategoriaService(self.categoria_repo, self.chamado_repo)


def create_app(com_dados_de_exemplo: bool = True) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sgc-ti-apresentacao"

    servicos = Servicos()
    if com_dados_de_exemplo:
        carregar_dados_de_exemplo(servicos)
    app.extensions["sgc"] = servicos

    from web.routes import bp
    app.register_blueprint(bp)
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
