# biblioteca-db

  ## Páginas necessárias

  - Página `/dashboard/*` de usuário, deve conter:
    - Perfil do usuário, nome, email, etc
    - Empréstimos que ele fez com:
      - Data de devolução
      - Data de que pegou o livro
      - Multa (Se possuir)
      - Quantidade de dias Atrasados (Se possuir)
      - Tempo restante de empréstimo (Se não tiver passado do tempo)

  - Página `/login` deve conter:
    - Formulário para envio de dados na rota `/login` com método POST
    - Cabeçalho com links para navegação
  - Página `/cadastro` deve conter:
    - Formulário de Cadastro para envio de dados na rota `/cadastro`
  - Rota `/logout` deve realizar:
    - Deslogar o usuário da sessão flask
  - Página `/livros` deve conter:
    - Lista de todos os livros do banco
      - Botão para adicionar empréstimo (adm)
      - Botão para visualizar o livro
    - Barra de pesquisa
