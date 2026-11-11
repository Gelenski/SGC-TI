from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria


class AutenticacaoService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo
