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


def criar_usuario(uid, perfil=Perfil.SOLICITANTE):
    return Usuario(
        uid,
        uid.title(),
        f"{uid}@empresa.com",
        "Senha@123",
        perfil,
    )


class TestF09:

    def setup_method(self):
        self.categorias = CategoriaRepositoryEmMemoria()
        self.chamados = ChamadoRepositoryEmMemoria()
        self.service = CategoriaService(self.categorias, self.chamados)
        self.admin = criar_usuario("admin", Perfil.ADMIN)

    def test_cadastrar_categoria(self):
        categoria = self.service.cadastrar_categoria(
            self.admin, "Redes", "Problemas de rede"
        )
        assert categoria.nome == "Redes"

    def test_nao_cadastrar_categoria_vazia(self):
        with pytest.raises(NegocioException):
            self.service.cadastrar_categoria(self.admin, "")

    def test_nao_cadastrar_categoria_duplicada(self):
        self.service.cadastrar_categoria(self.admin, "Redes")
        with pytest.raises(NegocioException):
            self.service.cadastrar_categoria(self.admin, "Redes")

    def test_listar_categorias(self):
        self.categorias.salvar(Categoria("1", "Redes", ""))
        assert len(self.service.listar_categorias()) == 1

    def test_buscar_categoria(self):
        self.categorias.salvar(Categoria("1", "Redes", ""))
        assert self.service.buscar_categoria("1").nome == "Redes"

    def test_categoria_inexistente(self):
        with pytest.raises(ObjetoNaoEncontradoException):
            self.service.buscar_categoria("999")

    def test_usuario_sem_permissao(self):
        with pytest.raises(AcessoNegadoException):
            self.service.cadastrar_categoria(
                criar_usuario("joao"), "Hardware"
            )


class TestF10F11:

    def setup_method(self):
        self.repo = ChamadoRepositoryEmMemoria()
        self.service = ChamadoConsultaService(self.repo)

    def test_listar_chamados(self):
        assert self.service.listar_chamados() == []

    def test_buscar_chamado_inexistente(self):
        assert self.service.buscar_chamado("999") is None

    def test_filtrar_chamados_sem_resultados(self):
        assert self.service.filtrar_chamados(categoria="Redes") == []

    def test_filtrar_chamados_sem_filtros(self):
        assert self.service.filtrar_chamados() == []