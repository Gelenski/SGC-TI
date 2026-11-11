Funcionalidade: Abrir chamado
  Como qualquer usuário autenticado (Solicitante, Técnico ou Admin)
  Quero registrar um novo chamado
  Para relatar um problema ou solicitação de suporte

  Cenário: Abertura de chamado com sucesso
    Dado que estou autenticado no sistema
    E existe a categoria "Redes" disponível
    Quando crio um chamado com título "Sem acesso à internet", descrição "Cabo desconectado" e categoria "Redes"
    Então o chamado deve ser registrado com status inicial "ABERTO"
    E deve estar vinculado ao meu usuário como solicitante

  Cenário: Tentativa de abertura sem preencher campos obrigatórios
    Dado que estou autenticado no sistema
    Quando tento criar um chamado com título "" e sem selecionar categoria
    Então o chamado não deve ser criado
    E o sistema deve alertar que "Título e categoria são campos obrigatórios