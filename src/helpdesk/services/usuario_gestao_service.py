from helpdesk.domain.models import Usuario, Perfil
from helpdesk.domain.exceptions import AcessoNegadoException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria


class UsuarioGestaoService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo

    def excluir_usuario(self, executor: Usuario, usuario_id: str) -> str:
        if executor.perfil != Perfil.ADMIN:
            raise AcessoNegadoException("Acesso não autorizado")

        self.repo.remover(usuario_id)
        return "Usuário removido com sucesso"