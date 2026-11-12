import pytest
from helpdesk.domain.models import Perfil, Usuario, Categoria, StatusChamado
from helpdesk.domain.exceptions import AcessoNegadoException, NegocioException
from helpdesk.repositories.repositories import (
    UsuarioRepositoryEmMemoria,
    CategoriaRepositoryEmMemoria,
    ChamadoRepositoryEmMemoria,
)
from helpdesk.services.usuario_gestao_service import UsuarioGestaoService
from helpdesk.services.chamado_criacao_service import ChamadoCriacaoService

class TestExcluirUsuario:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = UsuarioRepositoryEmMemoria()
        self.service = UsuarioGestaoService(self.repo)

        # E existe um usuário cadastrado com ID "15"
        self.repo.salvar(
            Usuario(
                id="15",
                nome="Usuário Alvo",
                email="alvo@empresa.com",
                senha="Senha@123",
                perfil=Perfil.SOLICITANTE,
            )
        )

    def test_administrador_exclui_usuario_existente_com_sucesso(self):
        # Dado que estou autenticado como "ADMIN"
        admin = Usuario(id="1", nome="Admin", email="admin@empresa.com",
                        senha="Admin@123", perfil=Perfil.ADMIN)

        # Quando solicito a exclusão do usuário ID "15"
        mensagem = self.service.excluir_usuario(admin, "15")

        # Então o usuário ID "15" deve ser removido da base de dados
        assert self.repo.buscar_por_id("15") is None
        # E deve ser exibida a mensagem "Usuário removido com sucesso"
        assert mensagem == "Usuário removido com sucesso"

    def test_tecnico_tenta_excluir_um_usuario(self):
        # Dado que estou autenticado como "TECNICO"
        tecnico = Usuario(id="2", nome="Técnico", email="tecnico@empresa.com",
                          senha="Tec@123", perfil=Perfil.TECNICO)

        # Quando solicito a exclusão do usuário ID "15"
        # Então o sistema deve rejeitar a solicitação
        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.excluir_usuario(tecnico, "15")

        # E deve retornar erro "Acesso não autorizado"
        assert str(exc_info.value) == "Acesso não autorizado"
        # (o usuário continua na base)
        assert self.repo.buscar_por_id("15") is not None

class TestAbrirChamado:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.chamado_repo = ChamadoRepositoryEmMemoria()
        self.categoria_repo = CategoriaRepositoryEmMemoria()
        self.service = ChamadoCriacaoService(self.chamado_repo, self.categoria_repo)

        # Dado que estou autenticado no sistema
        self.usuario_logado = Usuario(id="user-luan", nome="Luan",
                                      email="luan@empresa.com", senha="Senha@123",
                                      perfil=Perfil.SOLICITANTE)

    def test_abertura_de_chamado_com_sucesso(self):
        # E existe a categoria "Redes" disponível
        self.categoria_repo.salvar(Categoria(id="cat-1", nome="Redes",
                                             descricao="Problemas de rede"))

        # Quando crio um chamado com título, descrição e categoria
        chamado = self.service.abrir_chamado(
            solicitante=self.usuario_logado,
            titulo="Sem acesso à internet",
            descricao="Cabo desconectado",
            nome_categoria="Redes",
        )

        # Então o chamado deve ser registrado com status inicial "ABERTO"
        assert chamado.status == StatusChamado.ABERTO
        assert self.chamado_repo.buscar_por_id(chamado.id) is not None
        assert chamado.titulo == "Sem acesso à internet"
        assert chamado.categoria.nome == "Redes"
        # E deve estar vinculado ao meu usuário como solicitante
        assert chamado.solicitante.id == "user-luan"

    def test_tentativa_de_abertura_sem_preencher_campos_obrigatorios(self):
        # Quando tento criar um chamado com título "" e sem selecionar categoria
        # Então o sistema deve alertar que os campos são obrigatórios
        with pytest.raises(NegocioException) as exc_info:
            self.service.abrir_chamado(
                solicitante=self.usuario_logado,
                titulo="",
                descricao="Qualquer descrição",
                nome_categoria=None,
            )

        assert str(exc_info.value) == "Título e categoria são campos obrigatórios"
        # E o chamado não deve ser criado
        assert self.chamado_repo.listar_todos() == []