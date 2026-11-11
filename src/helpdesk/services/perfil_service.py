from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria


class PerfilService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo
    