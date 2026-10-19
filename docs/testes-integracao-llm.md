# Testes de integração apoiados por LLM

## Cenário e método

Projeto: AssistantAct, base `13b078eff1dacaa2e68180c7f95f562e1dc3a4b2`.
Data do experimento: 19/10/2026 (Europe/Lisbon).
LLM utilizada: o assistente Codex desta conversa. Os prompts abaixo foram
formulados e processados nesta sessão; as respostas registradas são os casos
produzidos pelo próprio assistente a partir do código lido. Não foi realizada
uma segunda chamada independente a um provedor, nem usado o endpoint de
priorização da aplicação para gerar os testes. A versão exata do modelo não
foi registrada pelo ambiente.

Integração escolhida: requisição HTTP → FastAPI/Pydantic → ActivityService →
PriorityAdvisor → ActivityRepository em memória → resposta HTTP. Na criação,
o serviço calcula a prioridade antes de persistir. Não existe front-end neste
repositório. A fronteira HTTP do provedor externo é simulada; as demais camadas
são reais. Cada teste recebe um repositório novo.

## Contexto fornecido aos dois prompts

POST /activities retorna 201; título obrigatório com 3 a 100 caracteres.
Status: pending, in_progress, done, canceled. Prioridade: low, medium, high.
GET /activities lista registros; GET /activities/{UUID} busca um registro;
PUT atualiza parcialmente; DELETE retorna 204 sem corpo. UUID malformado ou
payload inválido retorna 422; UUID inexistente retorna 404.
Sem prioridade explícita, ActivityService usa PriorityAdvisor. Sem chave de
API, a heurística classifica consulta/terapia ou has_changes=true como high
e uma atividade simples, como Ler livro, como low. Na atualização sem
prioridade explícita, ela é recalculada usando o registro mesclado.
Com chave, PriorityAdvisor envia POST ao endereço base + /responses com model
e input, timeout de 2 segundos; prioridade válida prevalece sobre a heurística.
Timeout, URLError e palavra inválida devem usar o fallback local.

## Prompt 1 — geração de cenários funcionais

```text
Atue como engenheiro de testes de integração do AssistantAct. Use o contexto
acima e as implementações de activity_routes, ActivityService,
ActivityRepository, PriorityAdvisor e modelos Pydantic lidas nesta sessão.
Gere três casos que atravessem as camadas reais da API, serviço e repositório:
ciclo CRUD completo, prioridade explícita e recálculo de prioridade após uma
mudança. Para cada caso informe ID, pré-condições, dados, sequência HTTP e
resultados verificáveis, incluindo persistência. Não invente banco de dados,
autenticação nem endpoints. Evite depender do relógio e de uma API externa.
```

Resposta gerada pela LLM:

| ID | Pré-condição e dados | Passos | Resultados esperados |
| --- | --- | --- | --- |
| IT01 | Repositório vazio, sem chave; título Consulta de rotina | POST; GET por ID; GET lista; PUT status=done; GET; DELETE; GET e lista | 201, UUID válido, pending/high; leituras iguais ao registro; PUT 200 mantém título e preenche updated_at; GET confirma atualização; DELETE 204 sem corpo; GET 404 e lista vazia |
| IT02 | Chave fictícia e transporte monitorado; título Consulta, priority=low | POST | 201 e low apesar da heurística high; nenhuma chamada externa |
| IT03 | Repositório vazio, sem chave; título Ler livro | POST; PUT has_changes=true; GET | Criação low; atualização 200/high; GET confirma prioridade e mudança persistidas |

## Prompt 2 — geração de erros, dados e contratos

```text
Atue como engenheiro de testes de integração do AssistantAct, usando o mesmo
contexto. Gere casos de validação e resiliência: payload inválido, identificador
malformado ou inexistente, atualização inválida, sucesso do provedor e falhas
do provedor (timeout, erro de rede e prioridade fora do contrato).
Informe ID, dados concretos, passos e resultados HTTP e de persistência.
Para o provedor, simule somente urlopen e mantenha reais o classificador,
serviço e repositório. Verifique método, URL, modelo, conteúdo enviado e
timeout. Não faça chamadas externas reais nem use credenciais reais.
```

Resposta gerada pela LLM:

| ID | Pré-condição e dados | Passos | Resultados esperados |
| --- | --- | --- | --- |
| IT04 | Repositório vazio; {}, título ab, título de 101 caracteres, status invalid, priority urgent ou scheduled_time invalid | POST para cada payload; GET lista | 422 em cada variante; lista vazia |
| IT05 | Repositório vazio; ID invalid e UUID válido inexistente | GET, PUT status=done e DELETE para cada ID | 422 para invalid; 404 para UUID inexistente; nenhuma atividade criada |
| IT06 | Atividade Ler livro já criada | PUT status=invalid; GET | 422; leitura mantém todos os campos originais |
| IT07 | Chave fictícia, modelo test-model, base https://provider.invalid/v1; título Consulta; provedor simulado retorna output[].content[].text=medium | POST; GET | Transporte recebe POST /v1/responses, model correto, título Consulta, fallback high e timeout 2; API retorna 201/medium e persiste resposta |
| IT08 | Mesmo contexto de IT07; transporte lança TimeoutError ou URLError, ou retorna urgent | POST; GET em cada variante | 201/high pelo fallback; registro persistido; exatamente uma tentativa ao provedor |

## Automação e análise

Implementação: `tests/test_integration_llm.py`. Os oito casos produzem 20
execuções por parametrização. A implementação foi revisada contra o código:
usa UUID retornado pela API, não fixa timestamps, compara estado após cada
operação e evita substituir o serviço ou classificador por implementações falsas.
O transporte externo é substituído por um mock com retorno estruturado.

Executar a partir da raiz com Python 3.12 ou superior (a suíte existente usa
a sintaxe de genéricos `def run_async[T]`, indisponível no Python 3.11):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q tests/test_integration_llm.py
python -m pytest -q
```

Limites: ASGI em processo, persistência em memória e provedor simulado.
Os testes não demonstram conectividade real, comportamento de um modelo
remoto, durabilidade após reinício, concorrência ou desempenho. A geração
de casos por LLM nesta sessão é distinta da simulação do provedor nos testes.

## Resultado observado

Validação local com Python 3.14.8, pytest 8.4.2, FastAPI 0.150.0,
Pydantic 2.14.1 e HTTPX 0.28.1: `python -m pytest -q` retornou
`34 passed in 0.29s` (14 testes existentes e 20 novos).
Não foram feitas alterações no código de produção.
