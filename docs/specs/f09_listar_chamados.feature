Funcionalidade: Listar chamados
  Como um usuário do sistema
  Quero consultar a lista de chamados
  Para visualizar as ocorrências de acordo com o meu nível de acesso

  Cenário: Administrador visualiza todos os chamados existentes
    Dado que estou autenticado como "ADMIN"
    E existem chamados atribuídos a diferentes técnicos e chamados sem atribuição
    Quando solicito a listagem de chamados
    Então o sistema deve retornar a lista completa com todos os chamados do sistema

  Cenário: Técnico visualiza apenas os chamados atribuídos a ele
    Dado que estou autenticado como "TECNICO" com o nome "Pedro"
    E existem 2 chamados atribuídos a "Pedro" e 3 chamados atribuídos ao técnico "Lucas"
    Quando solicito a listagem de chamados
    Então o sistema deve retornar exatamente os 2 chamados atribuídos a "Pedro"
    E nenhum chamado atribuído a "Lucas" deve constar na listagem