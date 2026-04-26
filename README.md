# Agenda Diaria Assistida por IA

MVP de micro-API em FastAPI para gerenciamento de atividades de rotina, com foco em apoio a usuarios autistas por meio de agenda diaria, cartoes visuais, checklists, temporizadores, secao "o que mudou" e sugestao de prioridade assistida por IA.

## Objetivo

Fornecer uma base simples, testavel e extensivel para organizar atividades diarias com suporte contextual.

A API permite representar atividades da rotina, sugerir prioridade automaticamente e preparar a evolucao para recursos como cartoes visuais, checklists e gatilhos do tipo:

```text
se terca-feira = terapia
entao mostrar checklist de saida
```

## Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- Uvicorn
- Pytest
- HTTPX
- OpenAI API opcional para sugestao de prioridade

## Instalacao

### 1. Clone o repositorio

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependencias

Com Makefile:

```bash
make install
```

Ou diretamente com pip:

```bash
pip install -r requirements.txt
```

## Configuracao

A API funciona sem arquivo `.env` e sem chave da OpenAI. Nesse caso, a prioridade das atividades e sugerida por heuristica local.

Para habilitar a integracao opcional com LLM, copie o exemplo:

```bash
cp .env.example .env
```

Depois preencha `OPENAI_API_KEY` no arquivo `.env`. Nunca versionar `.env` com chave real.

## Execucao

Rode a API localmente:

```bash
make run
```

Ou diretamente com Uvicorn:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

URLs principais:

```text
API:  http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs
```

Healthcheck:

```bash
curl http://127.0.0.1:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "timestamp": "2026-04-25T00:00:00+00:00"
}
```

## Endpoints de Atividades

As rotas de atividades ficam em:

```text
/activities
```

Operacoes disponiveis:

```text
POST   /activities
GET    /activities
GET    /activities/{activity_id}
PUT    /activities/{activity_id}
DELETE /activities/{activity_id}
```

Codigos HTTP principais:

```text
201 Created      atividade criada
200 OK           consulta ou atualizacao concluida
204 No Content   atividade removida
404 Not Found    atividade nao encontrada
422 Unprocessable Entity payload invalido
```

### Criar atividade

```bash
curl -X POST http://127.0.0.1:8000/activities \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Saida para terapia",
    "description": "Preparar mochila e checklist de saida.",
    "period": "manha",
    "status": "pending",
    "has_changes": false
  }'
```

Resposta esperada:

```json
{
  "id": "8d584339-d9a8-4928-9588-ea49e8637957",
  "title": "Saida para terapia",
  "description": "Preparar mochila e checklist de saida.",
  "scheduled_time": null,
  "period": "manha",
  "status": "pending",
  "priority": "high",
  "visual_card_ids": [],
  "checklist_id": null,
  "timer_id": null,
  "has_changes": false,
  "created_at": "2026-04-25T22:44:20.856644Z",
  "updated_at": null
}
```

### Listar atividades

```bash
curl http://127.0.0.1:8000/activities
```

### Buscar atividade por ID

```bash
curl http://127.0.0.1:8000/activities/<activity_id>
```

### Atualizar atividade

```bash
curl -X PUT http://127.0.0.1:8000/activities/<activity_id> \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

### Remover atividade

```bash
curl -X DELETE http://127.0.0.1:8000/activities/<activity_id>
```

## Testes

Execute todos os testes:

```bash
make test
```

Ou diretamente com Pytest:

```bash
pytest
```

Suites especificas:

```bash
pytest tests/test_activity_service.py
pytest tests/test_priority_advisor.py
pytest tests/test_activity_routes.py
```

Os testes de rota usam `httpx.AsyncClient` com `ASGITransport` para exercitar a API sem depender de servidor HTTP externo.

## Arquitetura

Estrutura principal:

```text
app/
├── api/
│   └── activity_routes.py
├── models/
│   └── activity.py
├── repositories/
│   └── activity_repository.py
├── services/
│   ├── activity_service.py
│   └── priority_advisor.py
└── main.py
```

Fluxo principal:

```text
HTTP request
-> activity_routes
-> ActivityService
-> ActivityRepository
-> PriorityAdvisor
-> HTTP response
```

Camadas:

- `api`: expoe rotas HTTP e traduz erros para respostas da API.
- `models`: define contratos Pydantic de entrada e saida.
- `repositories`: concentra persistencia inicial em memoria.
- `services`: concentra regras de negocio.
- `PriorityAdvisor`: sugere prioridade por heuristica local ou IA opcional.

## Uso da IA

O projeto funciona sem custo de API por padrao.

Quando `OPENAI_API_KEY` nao esta configurada, o `PriorityAdvisor` usa heuristica local baseada em:

- termos como terapia, consulta, medicamento, saida e urgente;
- atividades proximas do horario atual;
- presenca de checklist ou temporizador;
- indicacao de mudanca na rotina.

Quando `OPENAI_API_KEY` esta configurada, a API chama o endpoint `/responses` da OpenAI para sugerir a prioridade da atividade. A IA nao cria atividades automaticamente; ela apenas classifica a prioridade como:

```text
low
medium
high
```

Variaveis usadas:

```env
OPENAI_API_KEY=
OPENAI_PRIORITY_MODEL=gpt-4.1-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

Exemplo de atividade que tende a receber prioridade alta:

```json
{
  "title": "Consulta medica",
  "description": "Separar documentos e sair com antecedencia.",
  "has_changes": true
}
```

A chamada externa possui timeout e fallback obrigatorio. Se a OpenAI falhar, demorar ou retornar valor invalido, a prioridade local e usada automaticamente.

## Limitacoes Atuais

- Persistencia apenas em memoria.
- Dados sao perdidos ao reiniciar a aplicacao.
- Ainda nao ha autenticacao ou autorizacao.
- Cartoes visuais, checklists, temporizadores e "o que mudou" ainda estao planejados para evolucao.
- Integracao com IA e opcional e limitada a sugestao de prioridade.
- Nao ha banco de dados, migrations ou camada de configuracao dedicada.

## Proximos Passos

- Implementar persistencia em banco de dados.
- Criar endpoints para cartoes visuais.
- Criar endpoints para checklists por atividade.
- Implementar temporizadores.
- Implementar secao "o que mudou".
- Evoluir gatilhos contextuais.
- Ampliar testes de validacao de payload e contratos HTTP.
- Preparar configuracao por ambiente.
- Definir estrategia de deploy.
