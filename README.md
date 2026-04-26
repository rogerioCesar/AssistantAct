# Agenda Diária Assistida por IA

MVP de micro-API em FastAPI para gerenciamento de atividades de rotina, com foco em apoio a usuários autistas por meio de agenda diária, cartões visuais, checklists, temporizadores, seção "o que mudou" e sugestão de prioridade assistida por IA.

## Objetivo

Fornecer uma base simples, testável e extensível para organizar atividades diárias com suporte contextual.

A API permite representar atividades da rotina, sugerir prioridade automaticamente e preparar a evolução para recursos como cartões visuais, checklists e gatilhos do tipo:

```text
se terça-feira = terapia
então mostrar checklist de saída
```

## Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- Uvicorn
- Pytest
- HTTPX
- OpenAI API opcional para sugestão de prioridade

## Instalação

### 1. Clone o repositório

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

### 3. Instale as dependências

Com Makefile:

```bash
make install
```

Ou diretamente com pip:

```bash
pip install -r requirements.txt
```

## Configuração

A API funciona sem arquivo `.env` e sem chave da OpenAI. Nesse caso, a prioridade das atividades é sugerida por heurística local.

Para habilitar a integração opcional com LLM, copie o exemplo:

```bash
cp .env.example .env
```

Depois preencha `OPENAI_API_KEY` no arquivo `.env`. Nunca versione `.env` com chave real.

## Execução

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

Operações disponíveis:

```text
POST   /activities
GET    /activities
GET    /activities/{activity_id}
PUT    /activities/{activity_id}
DELETE /activities/{activity_id}
```

Códigos HTTP principais:

```text
201 Created      atividade criada
200 OK           consulta ou atualização concluída
204 No Content   atividade removida
404 Not Found    atividade não encontrada
422 Unprocessable Entity payload inválido
```

### Criar atividade

```bash
curl -X POST http://127.0.0.1:8000/activities \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Saída para terapia",
    "description": "Preparar mochila e checklist de saída.",
    "period": "manhã",
    "status": "pending",
    "has_changes": false
  }'
```

Resposta esperada:

```json
{
  "id": "8d584339-d9a8-4928-9588-ea49e8637957",
  "title": "Saída para terapia",
  "description": "Preparar mochila e checklist de saída.",
  "scheduled_time": null,
  "period": "manhã",
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

Suítes específicas:

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

- `api`: expõe rotas HTTP e traduz erros para respostas da API.
- `models`: define contratos Pydantic de entrada e saída.
- `repositories`: concentra persistência inicial em memória.
- `services`: concentra regras de negócio.
- `PriorityAdvisor`: sugere prioridade por heurística local ou IA opcional.

## Uso da IA

O projeto funciona sem custo de API por padrão.

Quando `OPENAI_API_KEY` não está configurada, o `PriorityAdvisor` usa heurística local baseada em:

- termos como terapia, consulta, medicamento, saída e urgente;
- atividades próximas do horário atual;
- presença de checklist ou temporizador;
- indicação de mudança na rotina.

Quando `OPENAI_API_KEY` está configurada, a API chama o endpoint `/responses` da OpenAI para sugerir a prioridade da atividade. A IA não cria atividades automaticamente; ela apenas classifica a prioridade como:

```text
low
medium
high
```

Variáveis usadas:

```env
OPENAI_API_KEY=
OPENAI_PRIORITY_MODEL=gpt-4.1-mini
OPENAI_BASE_URL=https://api.openai.com/v1
```

Exemplo de atividade que tende a receber prioridade alta:

```json
{
  "title": "Consulta médica",
  "description": "Separar documentos e sair com antecedência.",
  "has_changes": true
}
```

A chamada externa possui timeout e fallback obrigatório. Se a OpenAI falhar, demorar ou retornar valor inválido, a prioridade local é usada automaticamente.

## Limitações Atuais

- Persistência apenas em memória.
- Dados são perdidos ao reiniciar a aplicação.
- Ainda não há autenticação ou autorização.
- Cartões visuais, checklists, temporizadores e "o que mudou" ainda estão planejados para evolução.
- Integração com IA é opcional e limitada à sugestão de prioridade.
- Não há banco de dados, migrations ou camada de configuração dedicada.

## Próximos Passos

- Implementar persistência em banco de dados.
- Criar endpoints para cartões visuais.
- Criar endpoints para checklists por atividade.
- Implementar temporizadores.
- Implementar seção "o que mudou".
- Evoluir gatilhos contextuais.
- Ampliar testes de validação de payload e contratos HTTP.
- Preparar configuração por ambiente.
- Definir estratégia de deploy.
