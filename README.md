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

- Python
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

```bash
pip install -r requirements.txt
```

## Execucao

Rode a API localmente:

```bash
uvicorn app.main:app --reload
```

Acesse a documentacao interativa:

```text
http://localhost:8000/docs
```

Healthcheck:

```text
GET /health
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

Operacoes previstas:

```text
POST   /activities
GET    /activities
GET    /activities/{activity_id}
PUT    /activities/{activity_id}
DELETE /activities/{activity_id}
```

Exemplo de criacao:

```json
{
  "title": "Saida para terapia",
  "description": "Preparar mochila e checklist de saida.",
  "status": "pending",
  "has_changes": false
}
```

## Testes

Execute todos os testes:

```bash
pytest
```

Ou rode suites especificas:

```bash
pytest tests/test_activity_service.py
pytest tests/test_priority_advisor.py
pytest tests/test_activity_routes.py
```

Observacao: os testes de rota usam `TestClient`. Caso haja incompatibilidade local entre versoes de Python, Starlette, AnyIO ou HTTPX, valide primeiro as versoes instaladas no ambiente virtual.

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

Camadas:

- `api`: expoe rotas HTTP e traduz erros para respostas da API.
- `models`: define contratos Pydantic de entrada e saida.
- `repositories`: concentra persistencia inicial em memoria.
- `services`: concentra regras de negocio.
- `PriorityAdvisor`: sugere prioridade por heuristica local ou IA opcional.

## Uso da IA

O projeto funciona sem custo de API por padrao.

Se `OPENAI_API_KEY` nao estiver configurada, o `PriorityAdvisor` usa heuristica local baseada em:

- termos como terapia, consulta, medicamento, saida e urgente;
- atividades proximas do horario atual;
- presenca de checklist ou temporizador;
- indicacao de mudanca na rotina.

Para habilitar chamada opcional a OpenAI:

```bash
export OPENAI_API_KEY="sua-chave"
```

Variaveis opcionais:

```bash
export OPENAI_PRIORITY_MODEL="gpt-4.1-mini"
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

A chamada externa possui timeout e fallback obrigatorio. Se a API externa falhar, demorar ou retornar valor invalido, a prioridade local e usada automaticamente.

Prioridades aceitas:

```text
low
medium
high
```

## Limitacoes Atuais

- Persistencia apenas em memoria.
- Dados sao perdidos ao reiniciar a aplicacao.
- Ainda nao ha autenticacao ou autorizacao.
- Rotas de atividades ainda precisam ser conectadas ao `app/main.py`.
- Cartoes visuais, checklists, temporizadores e "o que mudou" ainda estao planejados para evolucao.
- Integracao com IA e opcional e limitada a sugestao de prioridade.
- Nao ha banco de dados, migrations ou camada de configuracao dedicada.

## Proximos Passos

- Conectar `activity_routes` ao `app/main.py`.
- Adicionar testes automatizados ao pipeline de desenvolvimento.
- Implementar persistencia em banco de dados.
- Criar endpoints para cartoes visuais.
- Criar endpoints para checklists por atividade.
- Implementar temporizadores.
- Implementar secao "o que mudou".
- Evoluir gatilhos contextuais.
- Documentar exemplos completos de uso da API.
- Preparar configuracao por ambiente.
- Definir estrategia de deploy.
