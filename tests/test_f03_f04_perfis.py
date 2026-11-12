import pytest
from helpdesk.domain.models import Perfil, Usuario
from helpdesk.domain.exceptions import AcessoNegadoException, NegocioException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria
from helpdesk.services.perfil_service import PerfilService


def criar_usuario(id, nome, perfil):
    return Usuario(id=id, nome=nome, email=f"{id}@empresa.com",
                   senha="Senha@123", perfil=perfil)


class TestCadastrarTipoUsuario:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = UsuarioRepositoryEmMemoria()
        self.service = PerfilService(self.repo)
        self.admin = criar_usuario("admin", "Admin", Perfil.ADMIN)

    def test_administrador_cadastra_novo_perfil_com_sucesso(self):
        # Dado que estou autenticado como "ADMIN"
        # E não existe um perfil cadastrado com o nome "TECNICO"
        assert self.service.tipo_existe("TECNICO") is False

        # Quando solicito o cadastro do tipo de usuário "TECNICO" com descrição
        self.service.cadastrar_tipo_usuario(
            self.admin, "TECNICO", "Perfil com permissão para atender chamados"
        )

        # Então o perfil "TECNICO" deve ser registrado com sucesso no sistema
        # E deve ficar disponível para atribuição a novos usuários
        assert self.service.tipo_existe("TECNICO") is True
        assert "TECNICO" in self.service.listar_tipos()

    def test_tentativa_de_cadastro_com_nome_duplicado(self):
        # Dado que estou autenticado como "ADMIN"
        # E já existe um perfil cadastrado com o nome "TECNICO"
        self.service.cadastrar_tipo_usuario(self.admin, "TECNICO", "Atende chamados")

        # Quando tento cadastrar um novo tipo de usuário chamado "TECNICO"
        # Então o sistema deve recusar a operação
        with pytest.raises(NegocioException) as exc_info:
            self.service.cadastrar_tipo_usuario(self.admin, "TECNICO", "Outro")

        # E deve exibir a mensagem "Tipo de usuário já existente"
        assert str(exc_info.value) == "Tipo de usuário já existente"

    def test_usuario_nao_administrador_tenta_cadastrar_perfil(self):
        # Dado que estou autenticado como "SOLICITANTE"
        solicitante = criar_usuario("sol", "Solicitante", Perfil.SOLICITANTE)

        # Quando tento enviar dados para cadastrar um novo tipo de usuário
        # Então a ação deve ser bloqueada
        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.cadastrar_tipo_usuario(solicitante, "GESTOR", "Gestor de área")

        # E o sistema deve retornar o erro de permissão
        assert str(exc_info.value) == "Acesso negado: permissão de administrador necessária"
        assert self.service.tipo_existe("GESTOR") is False