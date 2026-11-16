Funcionalidade: Excluir usuário
  Como um administrador do sistema
  Quero excluir usuários da base
  Para remover acessos indevidos ou descontinuados

  Cenário: Administrador exclui usuário existente com sucesso
    Dado que estou autenticado como "ADMIN"
    E existe um usuário cadastrado com ID "15"
    Quando solicito a exclusão do usuário ID "15"
    Então o usuário ID "15" deve ser removido da base de dados
    E deve ser exibida a mensagem "Usuário removido com sucesso"

  Cenário: Técnico tenta excluir um usuário
    Dado que estou autenticado como "TECNICO"
    E existe um usuário cadastrado com ID "15"
    Quando solicito a exclusão do usuário ID "15"
    Então o sistema deve rejeitar a solicitação
    E deve retornar erro "Acesso não autorizado"