class NegocioException(Exception):
    """Exceção base para todas as regras de negócio violadas no sistema."""
    pass


class EmailJaCadastradoException(NegocioException):
    pass


class CredenciaisInvalidasException(NegocioException):
    pass


class AcessoNegadoException(NegocioException):
    pass


class ObjetoNaoEncontradoException(NegocioException):
    pass