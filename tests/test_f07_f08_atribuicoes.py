import pytest
from helpdesk.domain.models import Categoria, Chamado, Perfil, StatusChamado, Usuario
from helpdesk.domain.exceptions import AcessoNegadoException
from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria
from helpdesk.services.chamado_operacao_service import ChamadoOperacaoService


def criar_usuario(id, nome, perfil):
    return Usuario(id=id, nome=nome, email=f"{id}@empresa.com",
                   senha="Senha@123", perfil=perfil)


def criar_chamado(id, solicitante, status=StatusChamado.ABERTO, responsavel=None):
    return Chamado(id=id, titulo="Computador não liga", descricao="Sem imagem no monitor",
                   categoria=Categoria(id="c1", nome="Hardware", descricao="Problemas de hardware"),
                   solicitante=solicitante, status=status, responsavel=responsavel)


# ---------------------------------------------------------------- F07
class TestAssumirChamado:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = ChamadoRepositoryEmMemoria()
        self.service = ChamadoOperacaoService(self.repo)
        self.solicitante = criar_usuario("sol", "Solicitante", Perfil.SOLICITANTE)

        # E existe um chamado ID "201" com status "ABERTO" e sem responsável
        self.repo.salvar(criar_chamado("201", self.solicitante))

    def test_tecnico_assume_chamado_em_aberto_com_sucesso(self):
        # Dado que estou autenticado como "TECNICO"
        tecnico = criar_usuario("tec", "Técnico", Perfil.TECNICO)

        # Quando eu assumo o chamado ID "201"
        self.service.assumir_chamado(tecnico, "201")

        # Então o chamado "201" deve ter seu responsável definido como meu usuário
        chamado = self.repo.buscar_por_id("201")
        assert chamado.responsavel == tecnico
        # E o status do chamado deve mudar para "EM ATENDIMENTO"
        assert chamado.status == StatusChamado.EM_ATENDIMENTO

    def test_solicitante_tenta_assumir_um_chamado(self):
        # Dado que estou autenticado como "SOLICITANTE"
        # Quando tento assumir o chamado ID "201"
        # Então o sistema deve impedir a ação
        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.assumir_chamado(self.solicitante, "201")

        # E exibir o erro "Apenas técnicos podem assumir chamados"
        assert str(exc_info.value) == "Apenas técnicos podem assumir chamados"
        # (o chamado não foi alterado)
        chamado = self.repo.buscar_por_id("201")
        assert chamado.responsavel is None
        assert chamado.status == StatusChamado.ABERTO
