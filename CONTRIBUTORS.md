# Integrantes e contribuições

## Integrante

- **Nome:** João Luis
- **GitHub:** [@JohnLouisMaker](https://github.com/JohnLouisMaker)

## Contribuições

### João Luis (@JohnLouisMaker)

- **Desenvolvimento da API:** implementação da API REST de acervo de livros com FastAPI, separando responsabilidades entre controllers, services, repositories e domínio em `src/acervo/`. Entrega das operações para cadastrar, listar, consultar, atualizar e remover livros, com filtros por busca, categoria, status e ano de publicação, além de paginação e validações de entrada.
- **Tratamento de respostas:** definição dos códigos HTTP para os fluxos da API, incluindo sucesso, recurso não encontrado, conflito por ID duplicado e erros de validação; implementação também do endpoint de saúde `/health`.
- **Infraestrutura e execução:** criação do `Dockerfile` para construir a imagem da aplicação e do `docker-compose.yml` para configurar sua execução local e publicação da porta da API.
- **Integração contínua:** configuração do workflow do GitHub Actions em `.github/workflows/ci.yml`, automatizando a instalação das dependências, a execução dos testes `pytest`, a validação da configuração do Docker Compose e a construção da imagem.
- **Testes e desempenho:** criação dos testes automatizados da API com `pytest`, cobrindo operações principais, filtros, paginação, validações e respostas de erro; elaboração e execução de um smoke test com k6 para verificar o endpoint de listagem e registrar métricas como latência p95 e taxa de falhas.
- **Documentação:** elaboração do `README.md` com informações e instruções de execução, do ADR sobre a escolha do FastAPI e do repositório em memória, da especificação do contrato em `docs/openapi.yaml`, do relatório dos resultados do k6 em `docs/desempenho.md` e do registro de uso de IA em `docs/ia.md`.


