from typing import Optional, List, Dict
from helpdesk.domain.models import Usuario, Categoria, Chamado

class UsuarioRepositoryEmMemoria:
    def __init__(self):
        self._usuarios: Dict[str, Usuario] = {}

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        for usuario in self._usuarios.values():
            if usuario.email.lower() == email.lower():
                return usuario
        return None

    def buscar_por_id(self, user_id: str) -> Optional[Usuario]:
        return self._usuarios.get(user_id)

    def salvar(self, usuario: Usuario) -> Usuario:
        self._usuarios[usuario.id] = usuario
        return usuario

    def listar_todos(self) -> List[Usuario]:
        return list(self._usuarios.values())

    def remover(self, user_id: str) -> None:
        self._usuarios.pop(user_id, None)


class CategoriaRepositoryEmMemoria:
    def __init__(self):
        self._categorias: Dict[str, Categoria] = {}

    def buscar_por_nome(self, nome: str) -> Optional[Categoria]:
        for categoria in self._categorias.values():
            if categoria.nome.lower() == nome.lower():
                return categoria
        return None

    def buscar_por_id(self, cat_id: str) -> Optional[Categoria]:
        return self._categorias.get(cat_id)

    def salvar(self, categoria: Categoria) -> Categoria:
        self._categorias[categoria.id] = categoria
        return categoria

    def listar_todas(self) -> List[Categoria]:
        return list(self._categorias.values())

    def remover(self, cat_id: str) -> None:
        self._categorias.pop(cat_id, None)


class ChamadoRepositoryEmMemoria:
    def __init__(self):
        self._chamados: Dict[str, Chamado] = {}

    def buscar_por_id(self, chamado_id: str) -> Optional[Chamado]:
        return self._chamados.get(chamado_id)

    def salvar(self, chamado: Chamado) -> Chamado:
        self._chamados[chamado.id] = chamado
        return chamado

    def listar_todos(self) -> List[Chamado]:
        return list(self._chamados.values())

    def remover(self, chamado_id: str) -> None:
        self._chamados.pop(chamado_id, None)