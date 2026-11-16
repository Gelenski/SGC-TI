import pytest
from helpdesk.domain.models import Perfil, Usuario
from helpdesk.domain.exceptions import AcessoNegadoException, NegocioException
from helpdesk.repositories.repositories import UsuarioRepositoryEmMemoria
from helpdesk.services.perfil_service import PerfilService


def criar_usuario(id, nome, perfil):
    return Usuario(id=id, nome=nome, email=f"{id}@empresa.com",
                   senha="Senha@123", perfil=perfil)


class TestCadastrarTipoUsuario:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = UsuarioRepositoryEmMemoria()
        self.service = PerfilService(self.repo)
        self.admin = criar_usuario("admin", "Admin", Perfil.ADMIN)

    def test_administrador_cadastra_novo_perfil_com_sucesso(self):
        assert self.service.tipo_existe("TECNICO") is False

        self.service.cadastrar_tipo_usuario(
            self.admin, "TECNICO", "Perfil com permissão para atender chamados"
        )

        assert self.service.tipo_existe("TECNICO") is True
        assert "TECNICO" in self.service.listar_tipos()

    def test_tentativa_de_cadastro_com_nome_duplicado(self):
        self.service.cadastrar_tipo_usuario(self.admin, "TECNICO", "Atende chamados")

        with pytest.raises(NegocioException) as exc_info:
            self.service.cadastrar_tipo_usuario(self.admin, "TECNICO", "Outro")

        assert str(exc_info.value) == "Tipo de usuário já existente"

    def test_usuario_nao_administrador_tenta_cadastrar_perfil(self):
        solicitante = criar_usuario("sol", "Solicitante", Perfil.SOLICITANTE)

        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.cadastrar_tipo_usuario(solicitante, "GESTOR", "Gestor de área")

        assert str(exc_info.value) == "Acesso negado: permissão de administrador necessária"
        assert self.service.tipo_existe("GESTOR") is False

class TestAlterarPerfilUsuario:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo = UsuarioRepositoryEmMemoria()
        self.service = PerfilService(self.repo)

        self.repo.salvar(criar_usuario("joao", "João", Perfil.SOLICITANTE))

    def test_administrador_altera_perfil_de_solicitante_para_tecnico(self):
        admin = criar_usuario("admin", "Admin", Perfil.ADMIN)

        mensagem = self.service.alterar_perfil(admin, "joao", Perfil.TECNICO)

        assert self.repo.buscar_por_id("joao").perfil == Perfil.TECNICO
        assert mensagem == "Perfil atualizado com sucesso"

    def test_usuario_nao_administrador_tenta_alterar_perfil(self):
        solicitante = criar_usuario("sol", "Solicitante", Perfil.SOLICITANTE)

        with pytest.raises(AcessoNegadoException) as exc_info:
            self.service.alterar_perfil(solicitante, "joao", Perfil.ADMIN)

        assert str(exc_info.value) == "Acesso negado: permissão de administrador necessária"
        assert self.repo.buscar_por_id("joao").perfil == Perfil.SOLICITANTE
