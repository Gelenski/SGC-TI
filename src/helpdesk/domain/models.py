from enum import Enum
from dataclasses import dataclass
from typing import Optional


class Perfil(str, Enum):
    SOLICITANTE = "SOLICITANTE"
    TECNICO = "TECNICO"
    ADMIN = "ADMIN"


class StatusChamado(str, Enum):
    ABERTO = "ABERTO"
    EM_ATENDIMENTO = "EM_ATENDIMENTO"
    RESOLVIDO = "RESOLVIDO"


@dataclass
class Usuario:
    id: str
    nome: str
    email: str
    senha: str
    perfil: Perfil


@dataclass
class Categoria:
    id: str
    nome: str
    descricao: str


@dataclass
class Chamado:
    id: str
    titulo: str
    descricao: str
    categoria: Categoria
    solicitante: Usuario
    status: StatusChamado = StatusChamado.ABERTO
    responsavel: Optional[Usuario] = None