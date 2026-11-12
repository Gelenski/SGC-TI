from helpdesk.domain.models import Usuario, Perfil
from helpdesk.domain.exceptions import AcessoNegadoException, NegocioException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria


class PerfilService:
    def __init__(self, repo: UsuarioRepositoryEmMemoria):
        self.repo = repo
        self.tipos = {}

    def cadastrar_tipo_usuario(self, executor: Usuario, nome: str, descricao: str):
        if executor.perfil != Perfil.ADMIN:
            raise AcessoNegadoException("Acesso negado: permissão de administrador necessária")
        if nome in self.tipos:
            raise NegocioException("Tipo de usuário já existente")
        self.tipos[nome] = descricao

    def tipo_existe(self, nome: str) -> bool:
        return nome in self.tipos

    def listar_tipos(self):
        return list(self.tipos.keys())