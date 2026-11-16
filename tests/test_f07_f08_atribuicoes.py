import pytest
from helpdesk.domain.models import Categoria, Chamado, Perfil, StatusChamado, Usuario
from helpdesk.domain.exceptions import AcessoNegadoException, NegocioException
from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria
from helpdesk.services.chamado_operacao_service import ChamadoOperacaoService


def criar_usuario(id, nome, perfil):
    return Usuario(id=id, nome=nome, email=f"{id}@empresa.com",
                   senha="Senha@123", perfil=perfil)


def criar_chamado(id, solicitante, status=StatusChamado.ABERTO, responsavel=None):
    return Chamado(id=id, titulo="Computador não liga", descricao="Sem imagem no monitor",
                   categoria=Categoria(id="c1", nome="Hardware", descricao="Problemas de hardware"),
                   solicitante=solicitante, status=status, responsavel=responsavel)


class TestAssumirChamado:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = ChamadoRepositoryEmMemoria()
        self.service = ChamadoOperacaoService(self.repo)
        self.solicitante = criar_usuario("sol", "Solicitante", Perfil.SOLICITANTE)

        self.repo.salvar(criar_chamado("201", self.solicitante))

    def test_tecnico_assume_chamado_em_aberto_com_sucesso(self):
        tecnico = criar_usuario("tec", "Técnico", Perfil.TECNICO)

        self.service.assumir_chamado(tecnico, "201")

        chamado = self.repo.buscar_por_id("201")
        assert chamado.responsavel == tecnico
        assert chamado.status == StatusChamado.EM_ATENDIMENTO

    def test_solicitante_tenta_assumir_um_chamado(self):
        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.assumir_chamado(self.solicitante, "201")

        assert str(exc_info.value) == "Apenas técnicos podem assumir chamados"
        chamado = self.repo.buscar_por_id("201")
        assert chamado.responsavel is None
        assert chamado.status == StatusChamado.ABERTO


class TestDelegarChamado:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = ChamadoRepositoryEmMemoria()
        self.service = ChamadoOperacaoService(self.repo)
        self.admin = criar_usuario("admin", "Admin", Perfil.ADMIN)

        solicitante = criar_usuario("sol", "Solicitante", Perfil.SOLICITANTE)
        self.repo.salvar(criar_chamado("305", solicitante))

    def test_administrador_delega_chamado_para_tecnico_com_sucesso(self):
        lucas = criar_usuario("lucas", "Lucas", Perfil.TECNICO)

        self.service.delegar_chamado(self.admin, "305", lucas)

        chamado = self.repo.buscar_por_id("305")
        assert chamado.responsavel == lucas
        assert chamado.status == StatusChamado.EM_ATENDIMENTO

    def test_administrador_tenta_delegar_para_usuario_solicitante(self):
        mariana = criar_usuario("mariana", "Mariana", Perfil.SOLICITANTE)

        with pytest.raises(NegocioException) as exc_info:
            self.service.delegar_chamado(self.admin, "305", mariana)

        assert str(exc_info.value) == "O usuário atribuído deve possuir perfil de técnico"
        chamado = self.repo.buscar_por_id("305")
        assert chamado.responsavel is None
        assert chamado.status == StatusChamado.ABERTO
