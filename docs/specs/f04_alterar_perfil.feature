Funcionalidade: Alterar tipo de perfil de usuário
  Como um administrador do sistema
  Quero alterar o perfil de acesso de um usuário existente
  Para definir permissões de Solicitante, Técnico ou Administrador

  Cenário: Administrador altera perfil de solicitante para técnico com sucesso
    Dado que estou autenticado como "ADMIN"
    E existe um usuário "João" com o perfil "SOLICITANTE"
    Quando eu altero o perfil de "João" para "TECNICO"
    Então o perfil de "João" deve ser atualizado para "TECNICO"
    E deve ser exibida a mensagem "Perfil atualizado com sucesso"

  Cenário: Usuário não administrador tenta alterar perfil
    Dado que estou autenticado como "SOLICITANTE"
    E existe um usuário "João" cadastrado
    Quando tento alterar o perfil de "João" para "ADMIN"
    Então a operação deve ser bloqueada
    E o sistema deve retornar erro "Acesso negado: permissão de administrador necessária"