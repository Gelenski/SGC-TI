Funcionalidade: Cadastro de usuário
  Como um visitante do sistema
  Quero criar uma conta
  Para que eu possa utilizar a plataforma como solicitante

  Cenário: Cadastro com sucesso com perfil padrão solicitante
    Dado que estou na página de cadastro
    Quando preencho o nome "Carlos Silva", e-mail "carlos@empresa.com" e senha "Senha@123"
    Então meu usuário deve ser criado com sucesso

  Cenário: Tentativa de cadastro com e-mail já existente
    Dado que já existe um usuário cadastrado com o e-mail "carlos@empresa.com"
    Quando preencho o formulário de cadastro usando o e-mail "carlos@empresa.com"
    Então o sistema deve recusar o cadastro
    E deve exibir a mensagem "E-mail já cadastrado no sistema"