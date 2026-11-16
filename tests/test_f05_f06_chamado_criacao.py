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
        admin = Usuario(id="1", nome="Admin", email="admin@empresa.com",
                        senha="Admin@123", perfil=Perfil.ADMIN)

        mensagem = self.service.excluir_usuario(admin, "15")

        assert self.repo.buscar_por_id("15") is None
        assert mensagem == "Usuário removido com sucesso"

    def test_tecnico_tenta_excluir_um_usuario(self):
        tecnico = Usuario(id="2", nome="Técnico", email="tecnico@empresa.com",
                          senha="Tec@123", perfil=Perfil.TECNICO)

        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.excluir_usuario(tecnico, "15")

        assert str(exc_info.value) == "Acesso não autorizado"
        assert self.repo.buscar_por_id("15") is not None

class TestAbrirChamado:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.chamado_repo = ChamadoRepositoryEmMemoria()
        self.categoria_repo = CategoriaRepositoryEmMemoria()
        self.service = ChamadoCriacaoService(self.chamado_repo, self.categoria_repo)

        self.usuario_logado = Usuario(id="user-luan", nome="Luan",
                                      email="luan@empresa.com", senha="Senha@123",
                                      perfil=Perfil.SOLICITANTE)

    def test_abertura_de_chamado_com_sucesso(self):
        self.categoria_repo.salvar(Categoria(id="cat-1", nome="Redes",
                                             descricao="Problemas de rede"))

        chamado = self.service.abrir_chamado(
            solicitante=self.usuario_logado,
            titulo="Sem acesso à internet",
            descricao="Cabo desconectado",
            nome_categoria="Redes",
        )

        assert chamado.status == StatusChamado.ABERTO
        assert self.chamado_repo.buscar_por_id(chamado.id) is not None
        assert chamado.titulo == "Sem acesso à internet"
        assert chamado.categoria.nome == "Redes"
        assert chamado.solicitante.id == "user-luan"

    def test_tentativa_de_abertura_sem_preencher_campos_obrigatorios(self):
        with pytest.raises(NegocioException) as exc_info:
            self.service.abrir_chamado(
                solicitante=self.usuario_logado,
                titulo="",
                descricao="Qualquer descrição",
                nome_categoria=None,
            )

        assert str(exc_info.value) == "Título e categoria são campos obrigatórios"
        assert self.chamado_repo.listar_todos() == []
