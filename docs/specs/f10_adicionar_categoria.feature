Funcionalidade: Adicionar categoria de chamado
  Como um administrador do sistema
  Quero cadastrar novas categorias de chamados
  Para classificar adequadamente os tipos de suporte

  Cenário: Cadastro de categoria com sucesso
    Dado que estou autenticado como "ADMIN"
    Quando cadastro uma nova categoria com o nome "Hardware" e descrição "Problemas físicos"
    Então a categoria "Hardware" deve ser salva no catálogo
    E deve estar disponível para seleção na abertura de chamados

  Cenário: Tentativa de cadastrar categoria com nome duplicado
    Dado que estou autenticado como "ADMIN"
    E já existe uma categoria cadastrada com o nome "Hardware"
    Quando tento cadastrar uma nova categoria chamada "Hardware"
    Então o sistema deve rejeitar o cadastro
    E deve exibir a mensagem "Categoria já existente"