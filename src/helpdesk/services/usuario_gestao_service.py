from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria


class UsuarioGestaoService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo
    