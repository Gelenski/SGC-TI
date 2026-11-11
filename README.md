# Sistema de Chamados de TI (SGC-TI)

Projeto acadêmico focado no desenvolvimento orientado por testes (**TDD**) a partir de especificações formais de comportamento baseadas em **BDD / Gherkin**[cite: 2].

---

## 🎯 Divisão de Responsabilidades

O escopo do sistema contempla 11 funcionalidades distribuídas entre os integrantes[cite: 1, 2]:

| Integrante | Funcionalidades | Módulo / Foco | Arquivo de Teste | Arquivo de Serviço |
| :--- | :--- | :--- | :--- | :--- |
| **Adrian Lazier**[cite: 2] | **F01, F02**[cite: 2] | Autenticação e Acesso Inicial[cite: 2] | `tests/test_f01_f02_autenticacao.py` | `src/helpdesk/services/autenticacao_service.py` |
| **Carlos Eduardo**[cite: 2] | **F03, F04**[cite: 2] | Gestão de Perfis e Permissões[cite: 2] | `tests/test_f03_f04_perfis.py` | `src/helpdesk/services/perfil_service.py` |
| **Luan Saviski**[cite: 2] | **F05, F06**[cite: 2] | Ciclo de Usuário e Criação de Chamado[cite: 2] | `tests/test_f05_f06_chamado_criacao.py` | `src/helpdesk/services/usuario_gestao_service.py`<br>`src/helpdesk/services/chamado_criacao_service.py` |
| **Lucas Gelenski**[cite: 2] | **F07, F08**[cite: 2] | Fluxo Operacional e Atribuições[cite: 2] | `tests/test_f07_f08_atribuicoes.py` | `src/helpdesk/services/chamado_operacao_service.py` |
| **João Augusto**[cite: 2] | **F09, F10, F11**[cite: 2] | Catálogo e Visualização com Filtros[cite: 2] | `tests/test_f09_f10_f11_catalogo.py` | `src/helpdesk/services/categoria_service.py`<br>`src/helpdesk/services/chamado_consulta_service.py` |

> As regras de negócio e os cenários de cada funcionalidade estão documentados em sintaxe Gherkin dentro da pasta `docs/specs/`[cite: 1, 2].

---

## 🏗️ Como Funciona a Arquitetura em Camadas

O projeto adota uma arquitetura em camadas desacoplada para garantir que a lógica de negócio possa ser testada sem dependência de banco de dados externo ou interfaces visuais:

```text
SGC-TI/
│
├── docs/specs/                  # 1. ESPECIFICAÇÕES BDD (Gherkin puro)
│   ├── f01_cadastro_usuario.feature
│   └── ... (até f11)
│
├── src/helpdesk/                # 2. O DOMÍNIO / REGRAS DE NEGÓCIO
│   ├── domain/                  # Entidades puras (Usuario, Chamado) e Exceções
│   │   ├── models.py
│   │   └── exceptions.py
│   ├── repositories/            # Persistência em memória compartilhada
│   │   └── repositories.py
│   └── services/                # Casos de uso (Onde cada integrante codifica)
│       ├── autenticacao_service.py
│       ├── perfil_service.py
│       ├── chamado_criacao_service.py
│       ├── usuario_gestao_service.py
│       ├── chamado_operacao_service.py
│       ├── categoria_service.py
│       └── chamado_consulta_service.py
│
├── tests/                       # 3. SUÍTE TDD (PyTest puro)
│   ├── conftest.py
│   ├── test_f01_f02_autenticacao.py
│   └── ... (arquivos isolados por integrante)
│
└── web/                         # 4. CAMADA DE APRESENTAÇÃO (Flask)
    ├── app.py
    ├── routes.py
    └── templates/