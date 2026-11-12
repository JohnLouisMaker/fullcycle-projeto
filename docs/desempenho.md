# Relatório de desempenho — Smoke Test Grafana k6

## Objetivo

Verificar a disponibilidade de `GET /livros` e medir a latência percebida durante uma carga leve e controlada. O SLO deste smoke test exige que o percentil 95 (`p95`) do tempo de resposta seja inferior a 200 ms e que a taxa de requisições com falha seja inferior a 1%. O teste também verifica o status HTTP e se cada resposta individual leva menos de 200 ms.

## Ambiente de execução

- **Sistema operacional:** Pop!\_OS 24.04 LTS (Linux x86_64; kernel `7.1.5-76070105-generic`).
- **Ferramenta:** Grafana k6 oficial, versão `v2.4.0` (`dd9395906d`, `linux/amd64`), baixada da release oficial do projeto.
- **Backend:** API FastAPI local, iniciada pelo Uvicorn existente no projeto, na porta 8000.
- **URL testada:** `http://127.0.0.1:8000/livros` (ambiente local, sem credenciais).
- **Conectividade prévia:** requisição inicial real retornou HTTP 200; corpo JSON com os três livros de exemplo.
- **Execução:** 12/11/2026, iniciada às 12:34:53 (-03:00); cenário local completado em 30,2 s.
- **Carga configurada:** 5 VUs durante 30 s; cada VU aguarda 1 s entre iterações.
- **Arquivo de teste:** [tests/k6-smoke-test.js](../tests/k6-smoke-test.js).
- **Saída integral capturada:** [tests/k6-smoke-output.txt](../tests/k6-smoke-output.txt).

A API foi testada localmente, não em produção. A contagem de iterações é diferente da contagem de requisições em geral; neste script, cada iteração emite uma requisição HTTP para `/livros`, então ambas totalizaram 150 nesta execução.

## Resultados reais

Valores transcritos da saída final do k6. Tempos em milissegundos, exceto RPS e porcentagens.

| Métrica                                     |              Resultado real |
| ------------------------------------------- | --------------------------: |
| Total de requisições HTTP (`http_reqs`)     |                         150 |
| Iterações completas (`iterations`)          |                         150 |
| Tempo médio (`avg`)                         |                     5,27 ms |
| Tempo mínimo (`min`)                        |      875,24 µs (0,87524 ms) |
| Tempo máximo (`max`)                        |                    42,15 ms |
| Mediana (`med`)                             |                     3,54 ms |
| p90                                         |                      6,9 ms |
| p95                                         |                     9,74 ms |
| p99                                         |                     41,5 ms |
| Requisições por segundo (`http_reqs`)       |                  4,967294/s |
| Taxa de falhas HTTP (`http_req_failed`)     |            0,00% — 0 de 150 |
| Checks aprovados                            |           300 de 300 (100%) |
| Checks reprovados                           |               0 de 300 (0%) |
| Check `GET /livros` retorna HTTP 200        | 150 aprovados; 0 reprovados |
| Check de tempo individual inferior a 200 ms | 150 aprovados; 0 reprovados |

O k6 contabiliza dois checks por requisição. `http_req_failed` mede falhas de requisição HTTP (por exemplo, erro de transporte ou resposta não considerada bem-sucedida), enquanto checks reprovados são validações do script; são métricas distintas. Não houve falhas HTTP nem falhas de validação nesta execução.

## Análise do SLO

- **p95 inferior a 200 ms:** **APROVADO** — valor observado de 9,74 ms; o k6 reportou o threshold `p(95)<200` aprovado.
- **Taxa de erros inferior a 1%:** **APROVADO** — valor observado de 0,00%; o k6 reportou o threshold `rate<0.01` aprovado.
- **Checks (`rate>0.99`):** **APROVADO** — 100,00%; 300 aprovados e nenhum reprovado.
- **Resultado geral:** **APROVADO**, conforme a saída da execução no terminal, que marcou os três thresholds com ✓.

## Conclusão

Na execução local registrada, a API respondeu às 150 requisições, todas com HTTP 200. O p95 observado foi 9,74 ms, abaixo do limite de 200 ms, e não houve falhas HTTP nem checks reprovados. Portanto, a API cumpriu os critérios deste smoke test sob a carga configurada. O resultado caracteriza somente esta execução local e não representa garantia de desempenho em produção, sob outra infraestrutura ou sob carga mais alta.

## Reprodutibilidade e evidências

O script usa `API_URL` para configurar a URL-base (padrão `http://localhost:8000`) e consulta `GET /livros`. Com a API em execução, pode-se repetir o teste com o binário oficial do k6 usando `API_URL=http://127.0.0.1:8000 k6 run tests/k6-smoke-test.js`.

A saída integral foi preservada em [tests/k6-smoke-output.txt](../tests/k6-smoke-output.txt). O k6 também gerou [tests/k6-smoke-summary.json](../tests/k6-smoke-summary.json); nesse JSON de resumo, os campos booleanos de `thresholds` aparecem como `false`, embora o resumo de execução no terminal marque os três thresholds como aprovados e mostre suas métricas dentro dos limites. Para não ocultar essa inconsistência do exportador, o arquivo JSON foi mantido como evidência auxiliar; a avaliação de aprovação neste relatório segue as linhas de resultado do k6 apresentadas no terminal, registradas integralmente no arquivo de saída acima.
