import pytest
from helpdesk.domain.models import Perfil, Usuario
from helpdesk.domain.exceptions import AcessoNegadoException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria
from helpdesk.services.usuario_gestao_service import UsuarioGestaoService


class TestExcluirUsuario:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = UsuarioRepositoryEmMemoria()
        self.service = UsuarioGestaoService(self.repo)

        # E existe um usuário cadastrado com ID "15"
        self.repo.salvar(
            Usuario(
                id="15",
                nome="Usuário Alvo",
                email="alvo@empresa.com",
                senha="Senha@123",
                perfil=Perfil.SOLICITANTE,
            )
        )

    def test_administrador_exclui_usuario_existente_com_sucesso(self):
        # Dado que estou autenticado como "ADMIN"
        admin = Usuario(id="1", nome="Admin", email="admin@empresa.com",
                        senha="Admin@123", perfil=Perfil.ADMIN)

        # Quando solicito a exclusão do usuário ID "15"
        mensagem = self.service.excluir_usuario(admin, "15")

        # Então o usuário ID "15" deve ser removido da base de dados
        assert self.repo.buscar_por_id("15") is None
        # E deve ser exibida a mensagem "Usuário removido com sucesso"
        assert mensagem == "Usuário removido com sucesso"

    def test_tecnico_tenta_excluir_um_usuario(self):
        # Dado que estou autenticado como "TECNICO"
        tecnico = Usuario(id="2", nome="Técnico", email="tecnico@empresa.com",
                          senha="Tec@123", perfil=Perfil.TECNICO)

        # Quando solicito a exclusão do usuário ID "15"
        # Então o sistema deve rejeitar a solicitação
        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.excluir_usuario(tecnico, "15")

        # E deve retornar erro "Acesso não autorizado"
        assert str(exc_info.value) == "Acesso não autorizado"
        # (o usuário continua na base)
        assert self.repo.buscar_por_id("15") is not None