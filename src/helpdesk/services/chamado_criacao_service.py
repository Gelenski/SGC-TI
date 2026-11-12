import uuid
from typing import Optional

from helpdesk.domain.models import Chamado, Usuario
from helpdesk.domain.exceptions import NegocioException
from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria, CategoriaRepositoryEmMemoria

MSG_CAMPOS_OBRIGATORIOS = "Título e categoria são campos obrigatórios"


class ChamadoCriacaoService:
    def __init__(self, chamado_repo: ChamadoRepositoryEmMemoria, categoria_repo: CategoriaRepositoryEmMemoria):
        self.chamado_repo = chamado_repo
        self.categoria_repo = categoria_repo

    def abrir_chamado(self, solicitante: Usuario, titulo: str, descricao: str,
                      nome_categoria: Optional[str]) -> Chamado:
        """F06 - Registra um novo chamado com status inicial ABERTO."""
        self._validar_campos_obrigatorios(titulo, nome_categoria)

        categoria = self.categoria_repo.buscar_por_nome(nome_categoria.strip())

        chamado = Chamado(
            id=self._gerar_id(),
            titulo=titulo.strip(),
            descricao=(descricao or "").strip(),
            categoria=categoria,
            solicitante=solicitante,
        )
        return self.chamado_repo.salvar(chamado)

    @staticmethod
    def _campo_vazio(valor: Optional[str]) -> bool:
        return valor is None or not valor.strip()

    def _validar_campos_obrigatorios(self, titulo: Optional[str], nome_categoria: Optional[str]) -> None:
        if self._campo_vazio(titulo) or self._campo_vazio(nome_categoria):
            raise NegocioException(MSG_CAMPOS_OBRIGATORIOS)

    @staticmethod
    def _gerar_id() -> str:
        return str(uuid.uuid4())[:8]