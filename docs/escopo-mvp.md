# Escopo do MVP

## Objetivo

Desenvolver uma micro-API para apoiar a organizacao de uma agenda diaria com cartoes visuais, temporizadores, checklists, secao de mudancas na rotina e gatilhos contextuais assistidos por IA.

O MVP deve permitir representar atividades do dia, associar apoios visuais e operacionais a cada atividade, indicar mudancas relevantes na rotina e aplicar regras simples como: "se hoje for terca-feira e houver terapia, mostrar checklist de saida".

## Requisitos Funcionais

### RF01 - Agenda diaria

A API deve permitir consultar a agenda diaria com a lista de atividades planejadas para uma data.

Cada atividade deve conter, no minimo:

- Identificador unico
- Titulo
- Descricao opcional
- Horario ou periodo sugerido
- Status da atividade
- Cartoes visuais associados
- Checklist associado, quando aplicavel
- Temporizador associado, quando aplicavel

### RF02 - Cartoes visuais

A API deve permitir cadastrar, consultar, atualizar e remover cartoes visuais.

Cada cartao visual deve conter, no minimo:

- Identificador unico
- Titulo
- Descricao opcional
- Tipo do cartao
- URL ou referencia visual
- Tags de contexto

### RF03 - Checklists

A API deve permitir criar e consultar checklists vinculados a atividades da rotina.

Cada checklist deve conter:

- Identificador unico
- Titulo
- Lista de itens
- Status de conclusao por item
- Atividade associada, quando aplicavel

### RF04 - Temporizadores

A API deve permitir associar temporizadores a atividades.

O MVP deve suportar:

- Duracao estimada da atividade
- Inicio do temporizador
- Pausa do temporizador
- Finalizacao do temporizador
- Consulta do status atual do temporizador

### RF05 - Secao "o que mudou"

A API deve permitir registrar mudancas na rotina diaria.

Cada mudanca deve conter:

- Identificador unico
- Data
- Descricao da mudanca
- Atividades impactadas
- Nivel de relevancia
- Mensagem curta para exibicao ao usuario

### RF06 - Gatilhos contextuais

A API deve permitir definir e aplicar gatilhos condicionais simples.

Exemplos de gatilhos:

- Se o dia da semana for terca-feira, mostrar checklist de saida para terapia.
- Se houver atividade escolar, mostrar cartoes de mochila, lanche e uniforme.
- Se houver mudanca na rotina, destacar a secao "o que mudou".

### RF07 - Apoio assistido por IA

A API deve prever integracao com IA para apoiar:

- Sugestao de checklists
- Sugestao de cartoes visuais
- Sugestao de adaptacoes para mudancas inesperadas
- Geracao de mensagens curtas e objetivas sobre mudancas na rotina

No MVP, a IA pode ser representada por uma camada de servico isolada, mesmo que inicialmente use respostas simuladas.

### RF08 - Healthcheck

A API deve expor um endpoint de verificacao de saude.

Endpoint minimo:

```text
GET /health
```

Resposta esperada:

```json
{
  "status": "ok",
  "timestamp": "2026-04-24T00:00:00+00:00"
}
```

## Requisitos Nao Funcionais

### RNF01 - Stack

A API deve ser desenvolvida em Python com FastAPI.

### RNF02 - Organizacao do codigo

O projeto deve manter separacao clara entre:

- Rotas
- Schemas
- Modelos
- Servicos
- Regras de negocio
- Testes

### RNF03 - Tipagem

O codigo deve usar tipagem explicita sempre que possivel.

### RNF04 - Validacao de dados

Entradas e saidas da API devem ser validadas com schemas Pydantic.

### RNF05 - Documentacao

A API deve manter documentacao interativa disponivel via OpenAPI/Swagger.

### RNF06 - Testabilidade

O MVP deve permitir testes automatizados para endpoints, regras de negocio e servicos principais.

### RNF07 - Baixo acoplamento

A camada de IA deve ser desacoplada das rotas e das regras centrais, permitindo troca futura do provedor.

### RNF08 - Seguranca basica

O MVP deve evitar exposicao de dados sensiveis em logs, respostas de erro e configuracoes versionadas.

### RNF09 - Configuracao por ambiente

Configuracoes sensiveis ou variaveis por ambiente devem ser carregadas por variaveis de ambiente.

### RNF10 - Execucao local simples

O projeto deve poder ser executado localmente com ambiente virtual e dependencias instaladas via `requirements.txt`.

## Fora de Escopo

- Interface web ou aplicativo mobile.
- Autenticacao e autorizacao de usuarios.
- Controle multiusuario ou perfis familiares.
- Persistencia definitiva em banco de dados relacional.
- Painel administrativo.
- Notificacoes push, SMS, e-mail ou WhatsApp.
- Integracao real obrigatoria com provedor de IA no primeiro incremento.
- Upload e armazenamento de imagens.
- Geracao automatica de imagens para cartoes visuais.
- Sincronizacao com calendarios externos.
- Deploy em ambiente de producao.
- Observabilidade avancada com metricas, tracing e alertas.
- Motor complexo de regras com linguagem propria.
- Personalizacao clinica ou terapeutica avancada.
