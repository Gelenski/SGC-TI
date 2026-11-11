import uuid
from helpdesk.domain.models import Usuario, Perfil
from helpdesk.domain.exceptions import (
    EmailJaCadastradoException,
    CredenciaisInvalidasException,
    NegocioException,
)
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria

class AutenticacaoService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo

    def cadastrar(self, nome: str, email: str, senha: str) -> Usuario:
        if not nome or not nome.strip():
            raise NegocioException("Nome é um campo obrigatório")
        if not email or not email.strip():
            raise NegocioException("E-mail é um campo obrigatório")
        if not senha or not senha.strip():
            raise NegocioException("Senha é um campo obrigatório")

        email_normalizado = email.strip().lower()

        if self.repo.buscar_por_email(email_normalizado):
            raise EmailJaCadastradoException("E-mail já cadastrado no sistema")

        novo_usuario = Usuario(
            id=str(uuid.uuid4())[:8],
            nome=nome.strip(),
            email=email_normalizado,
            senha=senha,
            perfil=Perfil.SOLICITANTE,
        )

        return self.repo.salvar(novo_usuario)

    def autenticar(self, email: str, senha: str) -> Usuario:
        if not email or not email.strip() or not senha or not senha.strip():
            raise CredenciaisInvalidasException("Credenciais inválidas")

        email_normalizado = email.strip().lower()
        usuario = self.repo.buscar_por_email(email_normalizado)

        if not usuario or usuario.senha != senha:
            raise CredenciaisInvalidasException("Credenciais inválidas")

        return usuario