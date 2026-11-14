from typing import Optional

from helpdesk.domain.exceptions import (
    AcessoNegadoException, NegocioException, ObjetoNaoEncontradoException,
)
from helpdesk.domain.models import Chamado, Perfil, StatusChamado, Usuario
from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria

MSG_APENAS_TECNICOS = "Apenas técnicos podem assumir chamados"
MSG_ACESSO_NEGADO_ADMIN = "Acesso negado: permissão de administrador necessária"
MSG_ATRIBUIDO_DEVE_SER_TECNICO = "O usuário atribuído deve possuir perfil de técnico"
MSG_CHAMADO_NAO_ENCONTRADO = "Chamado não encontrado"


class ChamadoOperacaoService:
    def __init__(self, chamado_repo: ChamadoRepositoryEmMemoria):
        self.chamado_repo = chamado_repo

    # ---------- F07 - Assumir chamado ----------
    def assumir_chamado(self, usuario: Optional[Usuario], chamado_id: str) -> None:
        """F07 - O técnico autenticado assume um chamado e passa a ser o responsável."""
        if not self._tem_perfil(usuario, Perfil.TECNICO):
            raise AcessoNegadoException(MSG_APENAS_TECNICOS)

        chamado = self._buscar_chamado(chamado_id)
        self._atribuir_responsavel(chamado, usuario)

    # ---------- F08 - Delegar chamado ----------
    def delegar_chamado(self, admin: Optional[Usuario], chamado_id: str,
                        tecnico: Optional[Usuario]) -> None:
        """F08 - O administrador delega um chamado para um técnico específico."""
        if not self._tem_perfil(admin, Perfil.ADMIN):
            raise AcessoNegadoException(MSG_ACESSO_NEGADO_ADMIN)
        if not self._tem_perfil(tecnico, Perfil.TECNICO):
            raise NegocioException(MSG_ATRIBUIDO_DEVE_SER_TECNICO)

        chamado = self._buscar_chamado(chamado_id)
        self._atribuir_responsavel(chamado, tecnico)

    # ---------- Métodos auxiliares ----------
    @staticmethod
    def _tem_perfil(usuario: Optional[Usuario], perfil: Perfil) -> bool:
        """Também trata usuário nulo (não autenticado) como sem permissão."""
        return usuario is not None and usuario.perfil == perfil

    def _buscar_chamado(self, chamado_id: str) -> Chamado:
        chamado = self.chamado_repo.buscar_por_id((chamado_id or "").strip())
        if chamado is None:
            raise ObjetoNaoEncontradoException(MSG_CHAMADO_NAO_ENCONTRADO)
        return chamado

    def _atribuir_responsavel(self, chamado: Chamado, tecnico: Usuario) -> None:
        """Regra comum a F07 e F08: define o responsável e coloca o chamado EM_ATENDIMENTO."""
        chamado.responsavel = tecnico
        chamado.status = StatusChamado.EM_ATENDIMENTO
        self.chamado_repo.salvar(chamado)
