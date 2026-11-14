from helpdesk.repositories.repositories import CategoriaRepositoryEmMemoria, ChamadoRepositoryEmMemoria


class CategoriaService:
    def __init__(self, categoria_repo: CategoriaRepositoryEmMemoria, chamado_repo: ChamadoRepositoryEmMemoria):
        self.categoria_repo = categoria_repo
        self.chamado_repo = chamado_repo
    
    def cadastrar_categoria(self, executor, nome, descricao=""):
        from helpdesk.domain.exceptions import NegocioException, AcessoNegadoException
        from helpdesk.domain.models import Categoria, Perfil
        import uuid

        if executor is None or executor.perfil != Perfil.ADMIN:
            raise AcessoNegadoException("Apenas administradores podem cadastrar categorias")

        nome = (nome or "").strip()

        if not nome:
            raise NegocioException("Nome da categoria é obrigatório")

        if self.categoria_repo.buscar_por_nome(nome):
            raise NegocioException("Categoria já cadastrada")

        categoria = Categoria(
            id=str(uuid.uuid4())[:8],
            nome=nome,
            descricao=(descricao or "").strip()
        )

        return self.categoria_repo.salvar(categoria)

    def listar_categorias(self):
        return sorted(
            self.categoria_repo.listar_todas(),
            key=lambda categoria: categoria.nome.casefold()
        )

    def buscar_categoria(self, categoria_id):
        from helpdesk.domain.exceptions import ObjetoNaoEncontradoException

        categoria = self.categoria_repo.buscar_por_id(categoria_id)

        if categoria is None:
            raise ObjetoNaoEncontradoException("Categoria não encontrada")

        return categoria

    def remover_categoria(self, executor, categoria_id):
        from helpdesk.domain.exceptions import NegocioException, AcessoNegadoException
        from helpdesk.domain.models import Perfil

        if executor is None or executor.perfil != Perfil.ADMIN:
            raise AcessoNegadoException("Apenas administradores podem remover categorias")

        categoria = self.buscar_categoria(categoria_id)

        for chamado in self.chamado_repo.listar_todos():
            if chamado.categoria.id == categoria.id:
                raise NegocioException(
                    "Não é possível remover uma categoria vinculada a chamados"
                )

        self.categoria_repo.remover(categoria.id)

        return "Categoria removida com sucesso"