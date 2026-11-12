import uuid
from helpdesk.domain.models import Chamado, Usuario
from helpdesk.domain.exceptions import NegocioException
from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria, CategoriaRepositoryEmMemoria


class ChamadoCriacaoService:
    def __init__(self, chamado_repo: ChamadoRepositoryEmMemoria, categoria_repo: CategoriaRepositoryEmMemoria):
        self.chamado_repo = chamado_repo
        self.categoria_repo = categoria_repo

    def abrir_chamado(self, solicitante: Usuario, titulo: str, descricao: str, nome_categoria: str) -> Chamado:
        if not titulo or not nome_categoria:
            raise NegocioException("Título e categoria são campos obrigatórios")

        categoria = self.categoria_repo.buscar_por_nome(nome_categoria)

        chamado = Chamado(
            id=str(uuid.uuid4())[:8],
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
            solicitante=solicitante,
        )
        return self.chamado_repo.salvar(chamado)