# Sistema de Chamados de TI (SGC-TI)

Projeto acadêmico focado no desenvolvimento orientado por testes (**TDD**) a partir de especificações formais de comportamento baseadas em **BDD / Gherkin**.

---

## 🎯 Divisão de Responsabilidades

O escopo do sistema contempla 11 funcionalidades distribuídas entre os integrantes:

| Integrante | Funcionalidades | Módulo / Foco | Arquivo de Teste | Arquivo de Serviço |
| :--- | :--- | :--- | :--- | :--- |
| **Adrian Lazier** | **F01, F02** | Autenticação e Acesso Inicial | `tests/test_f01_f02_autenticacao.py` | `src/helpdesk/services/autenticacao_service.py` |
| **Carlos Eduardo** | **F03, F04** | Gestão de Perfis e Permissões | `tests/test_f03_f04_perfis.py` | `src/helpdesk/services/perfil_service.py` |
| **Luan Saviski** | **F05, F06** | Ciclo de Usuário e Criação de Chamado | `tests/test_f05_f06_chamado_criacao.py` | `src/helpdesk/services/usuario_gestao_service.py`<br>`src/helpdesk/services/chamado_criacao_service.py` |
| **Lucas Gelenski** | **F07, F08** | Fluxo Operacional e Atribuições | `tests/test_f07_f08_atribuicoes.py` | `src/helpdesk/services/chamado_operacao_service.py` |
| **João Augusto** | **F09, F10, F11** | Catálogo e Visualização com Filtros | `tests/test_f09_f10_f11_catalogo.py` | `src/helpdesk/services/categoria_service.py`<br>`src/helpdesk/services/chamado_consulta_service.py` |

> As regras de negócio e os cenários de cada funcionalidade estão documentados em sintaxe Gherkin dentro da pasta `docs/specs/`.

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
    ├── seed.py                  # Dados de exemplo para a apresentação
    └── templates/               # Telas HTML
```

---

## ▶️ Como rodar

### 1. Instalar as dependências
Na pasta raiz do projeto (de preferência dentro de um ambiente virtual):

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS
pip install -r requirements.txt
```

### 2. Rodar a suíte de testes (TDD)
```bash
python -m pytest -v
```

### 3. Rodar a interface web
```bash
python -m web.app
```
Abra **http://127.0.0.1:5000** no navegador. Para parar o servidor, use `Ctrl + C`.

Os dados ficam em memória: ao reiniciar o servidor, o sistema volta aos dados de exemplo.
Usuários de exemplo (senha `Senha@123` para todos):

| Usuário | E-mail | Perfil |
| :--- | :--- | :--- |
| Administrador | admin@empresa.com | ADMIN |
| Pedro | pedro@empresa.com | TECNICO |
| Lucas | lucas@empresa.com | TECNICO |
| Ana | ana@empresa.com | SOLICITANTE |
| Mariana | mariana@empresa.com | SOLICITANTE |

**Modo demonstração:** o botão no topo da tela mostra ações que normalmente ficam escondidas para o
perfil logado (por exemplo, "Assumir" para um solicitante). Assim é possível demonstrar os cenários
de exceção do Gherkin: o próprio service bloqueia a ação e a mensagem de erro aparece na tela.
