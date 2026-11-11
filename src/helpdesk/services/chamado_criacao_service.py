from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria, CategoriaRepositoryEmMemoria


class ChamadoCriacaoService:
    def __init__(self, chamado_repo: ChamadoRepositoryEmMemoria, categoria_repo: CategoriaRepositoryEmMemoria):
        self.chamado_repo = chamado_repo
        self.categoria_repo = categoria_repo
 