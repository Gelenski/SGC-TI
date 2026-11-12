from typing import Dict, List

from helpdesk.domain.models import Usuario, Perfil
from helpdesk.domain.exceptions import AcessoNegadoException, NegocioException, ObjetoNaoEncontradoException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria

MSG_ACESSO_NEGADO_ADMIN = "Acesso negado: permissão de administrador necessária"
MSG_TIPO_JA_EXISTENTE = "Tipo de usuário já existente"
MSG_PERFIL_ATUALIZADO = "Perfil atualizado com sucesso"
MSG_USUARIO_NAO_ENCONTRADO = "Usuário não encontrado"


class PerfilService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo
        self._tipos: Dict[str, str] = {}  # nome do tipo -> descrição

    # ---------- F03 - Cadastrar tipo de usuário ----------
    def cadastrar_tipo_usuario(self, executor: Usuario, nome: str, descricao: str) -> None:
        """F03 - Cadastra um novo tipo de perfil. Somente ADMIN pode executar."""
        self._garantir_que_e_admin(executor)

        nome_normalizado = self._normalizar(nome)
        if self.tipo_existe(nome_normalizado):
            raise NegocioException(MSG_TIPO_JA_EXISTENTE)

        self._tipos[nome_normalizado] = (descricao or "").strip()

    def tipo_existe(self, nome: str) -> bool:
        return self._normalizar(nome) in self._tipos

    def listar_tipos(self) -> List[str]:
        return list(self._tipos.keys())

    # ---------- F04 - Alterar perfil de usuário ----------
    def alterar_perfil(self, executor: Usuario, usuario_id: str, novo_perfil: Perfil) -> str:
        """F04 - Altera o perfil de acesso de um usuário. Somente ADMIN pode executar."""
        self._garantir_que_e_admin(executor)

        usuario = self.repo.buscar_por_id(usuario_id)
        if usuario is None:
            raise ObjetoNaoEncontradoException(MSG_USUARIO_NAO_ENCONTRADO)

        usuario.perfil = novo_perfil
        self.repo.salvar(usuario)
        return MSG_PERFIL_ATUALIZADO

    # ---------- Métodos auxiliares ----------
    @staticmethod
    def _normalizar(nome: str) -> str:
        return (nome or "").strip().upper()

    @staticmethod
    def _garantir_que_e_admin(executor: Usuario) -> None:
        """Validação de permissão reaproveitada por F03 e F04."""
        if executor is None or executor.perfil != Perfil.ADMIN:
            raise AcessoNegadoException(MSG_ACESSO_NEGADO_ADMIN)