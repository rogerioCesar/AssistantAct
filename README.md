# Agenda Diaria Assistida por IA

MVP de micro-API para uma agenda diaria com apoio visual, temporizadores, checklist, secao "o que mudou" e gatilhos inteligentes baseados em contexto.

## Objetivo

Criar uma API simples e extensivel para apoiar rotinas diarias por meio de cartoes visuais, tarefas guiadas e regras contextuais.

Exemplos de uso:

- Se hoje for terca-feira, exibir checklist de saida para terapia.
- Se houver mudanca na rotina, destacar a secao "o que mudou".
- Se uma atividade tiver duracao definida, disponibilizar temporizador.
- Se uma tarefa exigir preparacao, mostrar checklist visual.

## Stack

- Python
- FastAPI
- Uvicorn
- Pydantic
- IA para apoio a geracao de sugestoes, gatilhos e adaptacoes de rotina

## Como Rodar Localmente

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

### 4. Rode a API

```bash
uvicorn app.main:app --reload
```

### 5. Acesse a documentacao interativa

```text
http://localhost:8000/docs
```

## Estrutura Inicial Sugerida

```text
.
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── rules/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Funcionalidades do MVP

- Cadastro de cartoes visuais de rotina
- Listagem da agenda diaria
- Checklists por atividade
- Temporizadores associados a tarefas
- Secao "o que mudou" para destacar alteracoes na rotina
- Gatilhos condicionais simples
- Suporte assistido por IA para sugestoes de rotina

## Exemplos de Gatilhos

```text
se dia_da_semana = terca
entao mostrar checklist "saida para terapia"
```

```text
se atividade = escola
entao mostrar cartoes "mochila", "lanche", "uniforme"
```

```text
se houve_mudanca = verdadeiro
entao destacar secao "o que mudou"
```

## Roadmap de Releases

### v0.1.0 - Base da API

- Criar estrutura inicial FastAPI
- Implementar health check
- Definir modelos principais
- Criar endpoints basicos de agenda
- Adicionar documentacao inicial

### v0.2.0 - Cartoes e Checklists

- Implementar CRUD de cartoes visuais
- Implementar checklists por atividade
- Associar cartoes a itens de rotina
- Criar testes unitarios iniciais

### v0.3.0 - Temporizadores

- Adicionar temporizadores por atividade
- Definir duracao estimada das tarefas
- Criar endpoints para iniciar, pausar e finalizar temporizadores
- Registrar status da atividade

### v0.4.0 - Mudancas na Rotina

- Implementar secao "o que mudou"
- Permitir marcacao de alteracoes no dia
- Destacar mudancas relevantes na agenda
- Adicionar historico simples de mudancas

### v0.5.0 - Gatilhos Contextuais

- Criar motor simples de regras condicionais
- Implementar gatilhos por dia da semana
- Implementar gatilhos por atividade
- Adicionar exemplos de regras predefinidas

### v0.6.0 - Apoio por IA

- Integrar servico de IA para sugestoes de rotina
- Gerar checklists assistidos por contexto
- Sugerir adaptacoes para mudancas inesperadas
- Registrar prompts e respostas relevantes

### v1.0.0 - MVP Estavel

- Consolidar endpoints principais
- Melhorar validacoes e tratamento de erros
- Adicionar testes de integracao
- Preparar documentacao para uso inicial em produto
- Definir guia basico de deploy
