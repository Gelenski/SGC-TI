Funcionalidade: Cadastrar tipo de usuário
  Como um administrador do sistema
  Quero cadastrar novos tipos de perfil de usuário
  Para expandir os níveis de acesso e permissões na plataforma

  Cenário: Administrador cadastra um novo perfil com sucesso
    Dado que estou autenticado como "ADMIN"
    E não existe um perfil cadastrado com o nome "TECNICO"
    Quando solicito o cadastro do tipo de usuário "TECNICO" com descrição "Perfil com permissão para atender chamados"
    Então o perfil "TECNICO" deve ser registrado com sucesso no sistema
    E deve ficar disponível para atribuição a novos usuários

  Cenário: Tentativa de cadastro com nome duplicado
    Dado que estou autenticado como "ADMIN"
    E já existe um perfil cadastrado com o nome "TECNICO"
    Quando tento cadastrar um novo tipo de usuário chamado "TECNICO"
    Então o sistema deve recusar a operação
    E deve exibir a mensagem "Tipo de usuário já existente"

  Cenário: Usuário não administrador tenta cadastrar perfil
    Dado que estou autenticado como "SOLICITANTE"
    Quando tento enviar dados para cadastrar um novo tipo de usuário
    Então a ação deve ser bloqueada
    E o sistema deve retornar o erro "Acesso negado: permissão de administrador necessária"