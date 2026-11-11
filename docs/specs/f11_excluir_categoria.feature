Funcionalidade: Excluir categoria de chamado
  Como um administrador do sistema
  Quero excluir uma categoria existente
  Para manter o catálogo de serviços atualizado

  Cenário: Excluir categoria sem chamados vinculados com sucesso
    Dado que estou autenticado como "ADMIN"
    E existe a categoria "Impressoras" que não possui nenhum chamado vinculado
    Quando solicito a exclusão da categoria "Impressoras"
    Então a categoria deve ser removida do sistema com sucesso

  Cenário: Impedir exclusão de categoria com chamados vinculados
    Dado que estou autenticado como "ADMIN"
    E existe a categoria "Redes" associada a pelo menos um chamado ativo
    Quando solicito a exclusão da categoria "Redes"
    Então a exclusão não deve ser permitida
    E o sistema deve alertar "Não é possível excluir uma categoria associada a chamados existentes"