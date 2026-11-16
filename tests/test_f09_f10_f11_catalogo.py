import pytest

from helpdesk.domain.exceptions import (
    AcessoNegadoException,
    NegocioException,
    ObjetoNaoEncontradoException,
)
from helpdesk.domain.models import (
    Categoria,
    Chamado,
    Perfil,
    StatusChamado,
    Usuario,
)
from helpdesk.repositories.repositories import (
    CategoriaRepositoryEmMemoria,
    ChamadoRepositoryEmMemoria,
)
from helpdesk.services.categoria_service import CategoriaService
from helpdesk.services.chamado_consulta_service import ChamadoConsultaService
from helpdesk.services.chamado_criacao_service import ChamadoCriacaoService


def criar_usuario(uid, perfil=Perfil.SOLICITANTE):
    return Usuario(
        uid,
        uid.title(),
        f"{uid}@empresa.com",
        "Senha@123",
        perfil,
    )


def criar_chamado(cid, categoria, solicitante, responsavel=None):
    status = StatusChamado.EM_ATENDIMENTO if responsavel else StatusChamado.ABERTO
    return Chamado(cid, f"Chamado {cid}", "", categoria, solicitante, status, responsavel)


# ---------------------------------------------------------------------------
# F09 - Listar chamados (docs/specs/f09_listar_chamados.feature)
# ---------------------------------------------------------------------------
class TestF09ListarChamados:

    def setup_method(self):
        self.repo = ChamadoRepositoryEmMemoria()
        self.service = ChamadoConsultaService(self.repo)
        self.solicitante = criar_usuario("ana")
        self.pedro = criar_usuario("pedro", Perfil.TECNICO)
        self.lucas = criar_usuario("lucas", Perfil.TECNICO)
        self.redes = Categoria("c1", "Redes", "")

    def test_administrador_visualiza_todos_os_chamados_existentes(self):
        self.repo.salvar(criar_chamado("1", self.redes, self.solicitante, self.pedro))
        self.repo.salvar(criar_chamado("2", self.redes, self.solicitante, self.lucas))
        self.repo.salvar(criar_chamado("3", self.redes, self.solicitante))

        chamados = self.service.listar_chamados()

        assert [c.id for c in chamados] == ["1", "2", "3"]

    def test_tecnico_visualiza_apenas_os_chamados_atribuidos_a_ele(self):
        for cid in ("1", "2"):
            self.repo.salvar(criar_chamado(cid, self.redes, self.solicitante, self.pedro))
        for cid in ("3", "4", "5"):
            self.repo.salvar(criar_chamado(cid, self.redes, self.solicitante, self.lucas))

        chamados = self.service.filtrar_chamados(responsavel_id=self.pedro.id)

        assert len(chamados) == 2
        assert all(c.responsavel.id == self.pedro.id for c in chamados)
        assert not any(c.responsavel.id == self.lucas.id for c in chamados)

    def test_listar_sem_chamados_retorna_lista_vazia(self):
        assert self.service.listar_chamados() == []

    def test_buscar_chamado_inexistente(self):
        assert self.service.buscar_chamado("999") is None

    def test_filtrar_chamados_sem_resultados(self):
        assert self.service.filtrar_chamados(categoria="Redes") == []


# ---------------------------------------------------------------------------
# F10 - Adicionar categoria (docs/specs/f10_adicionar_categoria.feature)
# ---------------------------------------------------------------------------
class TestF10AdicionarCategoria:

    def setup_method(self):
        self.categorias = CategoriaRepositoryEmMemoria()
        self.chamados = ChamadoRepositoryEmMemoria()
        self.service = CategoriaService(self.categorias, self.chamados)
        self.admin = criar_usuario("admin", Perfil.ADMIN)

    def test_cadastro_de_categoria_com_sucesso(self):
        categoria = self.service.cadastrar_categoria(
            self.admin, "Hardware", "Problemas físicos"
        )

        assert categoria.nome == "Hardware"
        assert self.categorias.buscar_por_nome("Hardware") is not None

        # E deve estar disponível para seleção na abertura de chamados
        criacao = ChamadoCriacaoService(self.chamados, self.categorias)
        chamado = criacao.abrir_chamado(criar_usuario("ana"), "Mouse quebrado", "", "Hardware")
        assert chamado.categoria.nome == "Hardware"

    def test_tentativa_de_cadastrar_categoria_com_nome_duplicado(self):
        self.service.cadastrar_categoria(self.admin, "Hardware")

        with pytest.raises(NegocioException, match="Categoria já existente"):
            self.service.cadastrar_categoria(self.admin, "Hardware")

    def test_nao_cadastrar_categoria_vazia(self):
        with pytest.raises(NegocioException):
            self.service.cadastrar_categoria(self.admin, "")

    def test_usuario_sem_permissao(self):
        with pytest.raises(AcessoNegadoException):
            self.service.cadastrar_categoria(criar_usuario("joao"), "Hardware")

    def test_listar_categorias(self):
        self.categorias.salvar(Categoria("1", "Redes", ""))
        assert len(self.service.listar_categorias()) == 1

    def test_buscar_categoria(self):
        self.categorias.salvar(Categoria("1", "Redes", ""))
        assert self.service.buscar_categoria("1").nome == "Redes"

    def test_categoria_inexistente(self):
        with pytest.raises(ObjetoNaoEncontradoException):
            self.service.buscar_categoria("999")


# ---------------------------------------------------------------------------
# F11 - Excluir categoria (docs/specs/f11_excluir_categoria.feature)
# ---------------------------------------------------------------------------
class TestF11ExcluirCategoria:

    def setup_method(self):
        self.categorias = CategoriaRepositoryEmMemoria()
        self.chamados = ChamadoRepositoryEmMemoria()
        self.service = CategoriaService(self.categorias, self.chamados)
        self.admin = criar_usuario("admin", Perfil.ADMIN)

    def test_excluir_categoria_sem_chamados_vinculados_com_sucesso(self):
        impressoras = self.categorias.salvar(Categoria("c1", "Impressoras", ""))

        self.service.remover_categoria(self.admin, impressoras.id)

        assert self.categorias.buscar_por_id(impressoras.id) is None

    def test_impedir_exclusao_de_categoria_com_chamados_vinculados(self):
        redes = self.categorias.salvar(Categoria("c2", "Redes", ""))
        self.chamados.salvar(criar_chamado("1", redes, criar_usuario("ana")))

        with pytest.raises(
            NegocioException,
            match="Não é possível excluir uma categoria associada a chamados existentes",
        ):
            self.service.remover_categoria(self.admin, redes.id)

        assert self.categorias.buscar_por_id(redes.id) is not None
