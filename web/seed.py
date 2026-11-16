from helpdesk.domain.models import Usuario, Perfil

SENHA_PADRAO = "Senha@123"

USUARIOS = [
    ("u-admin", "Administrador", "admin@empresa.com", Perfil.ADMIN),
    ("u-pedro", "Pedro", "pedro@empresa.com", Perfil.TECNICO),
    ("u-lucas", "Lucas", "lucas@empresa.com", Perfil.TECNICO),
    ("u-ana", "Ana", "ana@empresa.com", Perfil.SOLICITANTE),
    ("u-mariana", "Mariana", "mariana@empresa.com", Perfil.SOLICITANTE),
]

CATEGORIAS = [
    ("Redes", "Problemas de conexão e internet"),
    ("Hardware", "Problemas físicos em equipamentos"),
    ("Software", "Instalação e erros de programas"),
    ("Impressoras", "Categoria sem chamados (pode ser excluída)"),
]

CHAMADOS = [
    ("u-ana", "Sem acesso à internet", "Cabo desconectado", "Redes", None),
    ("u-ana", "Mouse não funciona", "Mouse parou de responder", "Hardware", "u-pedro"),
    ("u-mariana", "Erro ao abrir o Excel", "Mensagem de licença expirada", "Software", "u-pedro"),
    ("u-mariana", "Wi-Fi instável", "Conexão cai a cada 10 minutos", "Redes", "u-lucas"),
    ("u-ana", "Monitor piscando", "Tela pisca ao ligar", "Hardware", None),
]


def carregar_dados_de_exemplo(servicos) -> None:
    for user_id, nome, email, perfil in USUARIOS:
        servicos.usuario_repo.salvar(
            Usuario(id=user_id, nome=nome, email=email, senha=SENHA_PADRAO, perfil=perfil)
        )

    admin = servicos.usuario_repo.buscar_por_id("u-admin")

    for nome, descricao in CATEGORIAS:
        servicos.categoria.cadastrar_categoria(admin, nome, descricao)

    servicos.perfil.cadastrar_tipo_usuario(admin, "SOLICITANTE", "Abre e acompanha chamados")
    servicos.perfil.cadastrar_tipo_usuario(admin, "TECNICO", "Atende chamados")
    servicos.perfil.cadastrar_tipo_usuario(admin, "ADMIN", "Gerencia o sistema")

    for solicitante_id, titulo, descricao, categoria, responsavel_id in CHAMADOS:
        solicitante = servicos.usuario_repo.buscar_por_id(solicitante_id)
        chamado = servicos.chamado_criacao.abrir_chamado(solicitante, titulo, descricao, categoria)
        if responsavel_id:
            tecnico = servicos.usuario_repo.buscar_por_id(responsavel_id)
            servicos.chamado_operacao.assumir_chamado(tecnico, chamado.id)
