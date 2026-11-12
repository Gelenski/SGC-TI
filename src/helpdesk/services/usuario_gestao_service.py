from helpdesk.domain.models import Usuario, Perfil
from helpdesk.domain.exceptions import AcessoNegadoException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria

MSG_ACESSO_NAO_AUTORIZADO = "Acesso não autorizado"
MSG_USUARIO_REMOVIDO = "Usuário removido com sucesso"


class UsuarioGestaoService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo

    def excluir_usuario(self, executor: Usuario, usuario_id: str) -> str:
        """F05 - Remove um usuário da base. Somente ADMIN pode executar."""
        self._garantir_que_e_admin(executor)

        self.repo.remover(usuario_id.strip())
        return MSG_USUARIO_REMOVIDO

    @staticmethod
    def _garantir_que_e_admin(executor: Usuario) -> None:
        """Bloqueia a operação se quem executa não for ADMIN (ou não estiver autenticado)."""
        if executor is None or executor.perfil != Perfil.ADMIN:
            raise AcessoNegadoException(MSG_ACESSO_NAO_AUTORIZADO)