import pytest
from helpdesk.domain.models import Perfil, Usuario
from helpdesk.domain.exceptions import EmailJaCadastradoException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria
from helpdesk.services.autenticacao_service import AutenticacaoService
from helpdesk.domain.exceptions import CredenciaisInvalidasException

class TestCadastroUsuario:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = UsuarioRepositoryEmMemoria()
        self.service = AutenticacaoService(self.repo)

    def test_cadastro_com_sucesso_com_perfil_padrao_solicitante(self):
        nome = "Carlos Silva"
        email = "carlos@empresa.com"
        senha = "Senha@123"

        usuario = self.service.cadastrar(nome, email, senha)

        assert usuario is not None
        assert usuario.nome == "Carlos Silva"
        assert usuario.email == "carlos@empresa.com"
        assert usuario.perfil == Perfil.SOLICITANTE
        
        usuario_salvo = self.repo.buscar_por_email(email)
        assert usuario_salvo is not None
        assert usuario_salvo.email == email

    def test_tentativa_de_cadastro_com_email_ja_existente(self):
        email = "carlos@empresa.com"
        self.repo.salvar(
            Usuario(
                id="user-1",
                nome="Existente",
                email=email,
                senha="123",
                perfil=Perfil.SOLICITANTE,
            )
        )

        with pytest.raises(EmailJaCadastradoException) as exc_info:
            self.service.cadastrar("Carlos Silva", email, "Senha@123")

        assert str(exc_info.value) == "E-mail já cadastrado no sistema"

class TestLoginUsuario:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = UsuarioRepositoryEmMemoria()
        self.service = AutenticacaoService(self.repo)

    def test_login_com_sucesso(self):
        email = "ana@empresa.com"
        senha = "Segredo@123"
        self.repo.salvar(
            Usuario(
                id="user-ana",
                nome="Ana Souza",
                email=email,
                senha=senha,
                perfil=Perfil.SOLICITANTE,
            )
        )

        usuario_autenticado = self.service.autenticar(email, senha)

        assert usuario_autenticado is not None
        assert usuario_autenticado.email == email
        assert usuario_autenticado.nome == "Ana Souza"

    def test_tentativa_de_login_com_senha_incorreta(self):
        email = "ana@empresa.com"
        self.repo.salvar(
            Usuario(
                id="user-ana",
                nome="Ana Souza",
                email=email,
                senha="Segredo@123",
                perfil=Perfil.SOLICITANTE,
            )
        )

        with pytest.raises(CredenciaisInvalidasException) as exc_info:
            self.service.autenticar(email, "SenhaErrada")

        assert str(exc_info.value) == "Credenciais inválidas"
