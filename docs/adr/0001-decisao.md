# ADR 0001: FastAPI e repositório em memória

## Contexto

O projeto é uma API REST para cadastro e listagem de livros, desenvolvida incrementalmente como parte do curso Full Cycle. Nesta etapa, o foco é estabelecer uma estrutura simples, separada em Controller, Service e Repository, sem introduzir infraestrutura de persistência externa.

## Decisão

Adotar **FastAPI** como framework HTTP e implementar inicialmente o **repositório de livros em memória**.

O FastAPI foi escolhido por oferecer integração direta com tipagem e validação de dados, geração automática de documentação OpenAPI e uma implementação enxuta para APIs REST. Isso reduz o código de infraestrutura e facilita o teste e a exploração dos endpoints durante o desenvolvimento.

O repositório em memória foi escolhido para manter a etapa inicial autocontida e concentrada no fluxo entre as camadas e nas regras de negócio. O contrato de repositório isola o serviço dos detalhes de armazenamento, permitindo substituir a implementação por uma persistente posteriormente, sem transferir essa responsabilidade para o Controller ou para o domínio.

## Consequências

- O desenvolvimento e a execução local não exigem banco de dados nem serviços externos.
- A separação em camadas permite testar e evoluir regras de negócio independentemente da tecnologia de persistência.
- A documentação OpenAPI gerada pelo FastAPI facilita a inspeção manual e a integração com clientes.
- Os dados mantidos em memória são perdidos quando o processo é encerrado ou reiniciado.
- O armazenamento não é compartilhado entre instâncias da aplicação e não atende, por si só, a requisitos de durabilidade, escalabilidade horizontal ou persistência em produção.
- Ao surgir a necessidade de preservar dados, será necessário adicionar uma implementação persistente de repositório e definir sua configuração e estratégia de migração.
