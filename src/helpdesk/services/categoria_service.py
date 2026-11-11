from helpdesk.repositories.repositories import CategoriaRepositoryEmMemoria, ChamadoRepositoryEmMemoria


class CategoriaService:
    def __init__(self, categoria_repo: CategoriaRepositoryEmMemoria, chamado_repo: ChamadoRepositoryEmMemoria):
        self.categoria_repo = categoria_repo
        self.chamado_repo = chamado_repo
 