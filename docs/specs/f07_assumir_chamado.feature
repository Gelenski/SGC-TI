Funcionalidade: Assumir chamado
  Como um técnico de suporte
  Quero assumir a responsabilidade por um chamado aberto
  Para que eu comece o atendimento

  Cenário: Técnico assume chamado em aberto com sucesso
    Dado que estou autenticado como "TECNICO"
    E existe um chamado ID "201" com status "ABERTO" e sem responsável
    Quando eu assumo o chamado ID "201"
    Então o chamado "201" deve ter seu responsável definido como meu usuário
    E o status do chamado deve mudar para "EM ATENDIMENTO"

  Cenário: Solicitante tenta assumir um chamado
    Dado que estou autenticado como "SOLICITANTE"
    E existe um chamado ID "201" com status "ABERTO"
    Quando tento assumir o chamado ID "201"
    Então o sistema deve impedir a ação
    E exibir o erro "Apenas técnicos podem assumir chamados"