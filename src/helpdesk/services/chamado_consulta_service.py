from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria


class ChamadoConsultaService:
    def __init__(self, chamado_repo: ChamadoRepositoryEmMemoria):
        self.chamado_repo = chamado_repo
    