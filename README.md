# Projeto B — API de domínio único

API REST para gerenciamento de um acervo de livros, desenvolvida em Python com FastAPI como projeto do curso Full Cycle.

## Visão geral

A API permite cadastrar, consultar, atualizar e remover livros. A listagem oferece busca por título, autor ou categoria, filtros por categoria, status e ano de publicação, além de paginação por `limite` e `deslocamento`. A aplicação é organizada em camadas de Controller, Service e Repository, com persistência em memória e livros de exemplo carregados na inicialização. Os dados são reiniciados quando a aplicação é reiniciada.

## Pré-requisitos

- Docker com o plugin Docker Compose (`docker compose`)
- Python 3.12 ou superior, para executar os testes localmente

## Executar com Docker Compose

Na raiz do repositório, construa a imagem e inicie a API:

```bash
docker compose up --build
```

Por padrão, a API fica disponível em <http://localhost:8000>. Para explorar e testar os endpoints, acesse a documentação interativa em <http://localhost:8000/docs>. O endpoint <http://localhost:8000/health> verifica a disponibilidade do serviço.

Para executar em segundo plano, use `docker compose up --build -d`. Para interromper e remover o contêiner, execute `docker compose down`.

## Endpoints principais

- `GET /livros`: lista livros; aceita `busca`, `categoria`, `status`, `ano_publicacao`, `limite` e `deslocamento`.
- `POST /livros`: cadastra um livro; retorna `409` quando o ID já está cadastrado.
- `GET /livros/{livro_id}`: consulta um livro; retorna `404` quando não encontrado.
- `PUT /livros/{livro_id}`: atualiza um livro existente; retorna `404` quando não encontrado.
- `DELETE /livros/{livro_id}`: remove um livro existente; retorna `204` sem conteúdo ou `404` quando não encontrado.
- `GET /health`: informa o estado da API.

## Executar os testes

Crie e ative um ambiente virtual, instale as dependências da aplicação e as ferramentas de teste, e execute o `pytest`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt "httpx>=0.27,<1.0" "pytest>=8.0,<9.0"
pytest -q
```

No Windows PowerShell, ative o ambiente virtual com `.venv\Scripts\Activate.ps1`. Os testes usam o `TestClient` do FastAPI e não precisam que a API esteja rodando separadamente.

Para repetir o smoke test de desempenho, mantenha a API em execução, instale o [Grafana k6](https://grafana.com/docs/k6/latest/set-up/install-k6/) e execute `k6 run tests/k6-smoke-test.js`. O relatório e a saída da execução registrada estão listados abaixo.

## Documentação e evidências

- [ADR 0001 — decisão arquitetural](docs/adr/0001-decisao.md): registra a escolha do FastAPI e do repositório em memória, incluindo contexto e consequências.
- [Contrato OpenAPI](docs/openapi.yaml): especificação dos endpoints, parâmetros, modelos e respostas.
- [Relatório de desempenho](docs/desempenho.md): metodologia, critérios, métricas e resultado do smoke test com k6.
- [Registro de uso de IA](docs/ia.md): prompts e atividades de documentação assistidas por IA registrados para este projeto.
- [Integrantes e contribuições](CONTRIBUTORS.md): identificação do participante e resumo das entregas individuais.
- [Teste k6](tests/k6-smoke-test.js) e [saída registrada](tests/k6-smoke-output.txt): script e evidência da execução descrita no relatório.

## Integração contínua

O GitHub Actions executa os testes automatizados em pull requests para `main` e em pushes para as branches configuradas. O workflow também valida a configuração do Docker Compose e constrói a imagem da API.
