from helpdesk.domain.exceptions import (
    AcessoNegadoException, NegocioException, ObjetoNaoEncontradoException,
)
from helpdesk.domain.models import Perfil, StatusChamado, Usuario
from helpdesk.repositories.repositories import ChamadoRepositoryEmMemoria


class ChamadoOperacaoService:
    def __init__(self, chamado_repo: ChamadoRepositoryEmMemoria):
        self.chamado_repo = chamado_repo

    def assumir_chamado(self, usuario: Usuario, chamado_id: str) -> None:
        if usuario.perfil != Perfil.TECNICO:
            raise AcessoNegadoException("Apenas técnicos podem assumir chamados")
        chamado = self.chamado_repo.buscar_por_id(chamado_id)
        if chamado is None:
            raise ObjetoNaoEncontradoException("Chamado não encontrado")
        chamado.responsavel = usuario
        chamado.status = StatusChamado.EM_ATENDIMENTO
        self.chamado_repo.salvar(chamado)

    def delegar_chamado(self, admin: Usuario, chamado_id: str, tecnico: Usuario) -> None:
        if admin.perfil != Perfil.ADMIN:
            raise AcessoNegadoException("Acesso negado: permissão de administrador necessária")
        if tecnico.perfil != Perfil.TECNICO:
            raise NegocioException("O usuário atribuído deve possuir perfil de técnico")
        chamado = self.chamado_repo.buscar_por_id(chamado_id)
        if chamado is None:
            raise ObjetoNaoEncontradoException("Chamado não encontrado")
        chamado.responsavel = tecnico
        chamado.status = StatusChamado.EM_ATENDIMENTO
        self.chamado_repo.salvar(chamado)
