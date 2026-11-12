## Projeto B

Base do projeto do curso Full Cycle: construção incremental de uma API REST para gerenciamento de um acervo de livros.

## Escopo previsto

A API é desenvolvida em Python com FastAPI e oferece cadastro, consulta, atualização e remoção de livros. A listagem suporta busca por título/autor/categoria, filtros por categoria, status e ano de publicação, além de paginação por `limite` e `deslocamento`. A implementação é organizada em camadas de Controller, Service e Repository em memória, com livros de exemplo carregados na inicialização e testes automatizados. Os dados são reiniciados quando a aplicação reinicia.

## Executar e explorar

Com a aplicação em execução, acesse `/docs` para explorar e testar os endpoints pela documentação interativa do Swagger. O endpoint `/health` retorna o estado da API.

Rotas principais:

- `GET /livros`: lista com filtros opcionais (`busca`, `categoria`, `status`, `ano_publicacao`, `limite`, `deslocamento`).
- `POST /livros`: cadastra um livro; retorna `409` se o ID já existir.
- `GET /livros/{livro_id}`: consulta um livro; retorna `404` quando não encontrado.
- `PUT /livros/{livro_id}`: atualiza os dados de um livro existente.
- `DELETE /livros/{livro_id}`: remove um livro existente.

As validações automatizadas são executadas pelo GitHub Actions em cada pull request para `main`, incluindo testes, validação do Docker Compose e construção da imagem da API.
