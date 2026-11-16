Funcionalidade: Login de usuário
  Como um usuário cadastrado
  Quero autenticar minhas credenciais
  Para acessar as funcionalidades do sistema

  Cenário: Login efetuado com sucesso
    Dado que existe um usuário com e-mail "ana@empresa.com" e senha "Segredo@123"
    Quando eu tento autenticar com o e-mail "ana@empresa.com" e senha "Segredo@123"
    Então a autenticação deve ser realizada com sucesso
    E devo ter acesso à área restrita do sistema

  Cenário: Tentativa de login com senha incorreta
    Dado que existe um usuário com e-mail "ana@empresa.com" e senha "Segredo@123"
    Quando eu tento autenticar com o e-mail "ana@empresa.com" e senha "SenhaErrada"
    Então o sistema deve recusar o login
    E deve exibir a mensagem "Credenciais inválidas"