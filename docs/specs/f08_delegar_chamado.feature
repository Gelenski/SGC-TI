Funcionalidade: Delegar chamado
  Como um administrador do sistema
  Quero delegar a responsabilidade de um chamado para um técnico específico
  Para equilibrar a carga de trabalho da equipe

  Cenário: Administrador delega chamado para um técnico com sucesso
    Dado que estou autenticado como "ADMIN"
    E existe um técnico cadastrado chamado "Lucas"
    E existe um chamado ID "305" com status "ABERTO"
    Quando eu delego o chamado "305" para o técnico "Lucas"
    Então o responsável pelo chamado "305" deve ser "Lucas"
    E o status do chamado deve ser atualizado para "EM ATENDIMENTO"

  Cenário: Administrador tenta delegar chamado para usuário com perfil de solicitante
    Dado que estou autenticado como "ADMIN"
    E existe um usuário chamado "Mariana" com perfil "SOLICITANTE"
    E existe um chamado ID "305" com status "ABERTO"
    Quando tento delegar o chamado "305" para "Mariana"
    Então a delegação deve falhar
    E o sistema deve exibir a mensagem "O usuário atribuído deve possuir perfil de técnico"