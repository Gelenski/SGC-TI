"""
SGC-TI - Camada de apresentação (Flask).

Interface web simples para demonstrar as 11 funcionalidades do sistema.
Toda a regra de negócio continua nos services de src/helpdesk/services;
esta camada só recebe os dados do formulário, chama o service e mostra
o resultado (ou a mensagem de erro que o próprio service lançou).

Como rodar (a partir da pasta raiz do projeto):
    python -m web.app
Depois abra http://127.0.0.1:5000 no navegador.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for caminho in (RAIZ, RAIZ / "src"):
    if str(caminho) not in sys.path:
        sys.path.insert(0, str(caminho))

from flask import Flask  # noqa: E402

from helpdesk.repositories import (  # noqa: E402
    UsuarioRepositoryEmMemoria,
    CategoriaRepositoryEmMemoria,
    ChamadoRepositoryEmMemoria,
)
from helpdesk.services import (  # noqa: E402
    AutenticacaoService,
    PerfilService,
    UsuarioGestaoService,
    ChamadoCriacaoService,
    ChamadoOperacaoService,
    CategoriaService,
    ChamadoConsultaService,
)
from web.seed import carregar_dados_de_exemplo  # noqa: E402


class Servicos:
    """Monta repositórios e services uma única vez (os dados ficam em memória)."""

    def __init__(self):
        self.usuario_repo = UsuarioRepositoryEmMemoria()
        self.categoria_repo = CategoriaRepositoryEmMemoria()
        self.chamado_repo = ChamadoRepositoryEmMemoria()

        self.autenticacao = AutenticacaoService(self.usuario_repo)                  # F01, F02
        self.perfil = PerfilService(self.usuario_repo)                              # F03, F04
        self.usuario_gestao = UsuarioGestaoService(self.usuario_repo)               # F05
        self.chamado_criacao = ChamadoCriacaoService(self.chamado_repo,
                                                     self.categoria_repo)           # F06
        self.chamado_operacao = ChamadoOperacaoService(self.chamado_repo)           # F07, F08
        self.chamado_consulta = ChamadoConsultaService(self.chamado_repo)           # F09
        self.categoria = CategoriaService(self.categoria_repo, self.chamado_repo)   # F10, F11


def create_app(com_dados_de_exemplo: bool = True) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sgc-ti-apresentacao"

    servicos = Servicos()
    if com_dados_de_exemplo:
        carregar_dados_de_exemplo(servicos)
    app.extensions["sgc"] = servicos

    from web.routes import bp
    app.register_blueprint(bp)
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
