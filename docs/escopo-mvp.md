# Escopo do MVP

## Objetivo

Desenvolver uma micro-API para apoiar a organização de uma agenda diária com cartões visuais, temporizadores, checklists, seção de mudanças na rotina e gatilhos contextuais assistidos por IA.

O MVP deve permitir representar atividades do dia, associar apoios visuais e operacionais a cada atividade, indicar mudanças relevantes na rotina e aplicar regras simples como: "se hoje for terça-feira e houver terapia, mostrar checklist de saída".

## Requisitos Funcionais

### RF01 - Agenda diária

A API deve permitir consultar a agenda diária com a lista de atividades planejadas para uma data.

Cada atividade deve conter, no mínimo:

- Identificador único
- Título
- Descrição opcional
- Horário ou período sugerido
- Status da atividade
- Cartões visuais associados
- Checklist associado, quando aplicável
- Temporizador associado, quando aplicável

### RF02 - Cartões visuais

A API deve permitir cadastrar, consultar, atualizar e remover cartões visuais.

Cada cartão visual deve conter, no mínimo:

- Identificador único
- Título
- Descrição opcional
- Tipo do cartão
- URL ou referência visual
- Tags de contexto

### RF03 - Checklists

A API deve permitir criar e consultar checklists vinculados a atividades da rotina.

Cada checklist deve conter:

- Identificador único
- Título
- Lista de itens
- Status de conclusão por item
- Atividade associada, quando aplicável

### RF04 - Temporizadores

A API deve permitir associar temporizadores a atividades.

O MVP deve suportar:

- Duração estimada da atividade
- Início do temporizador
- Pausa do temporizador
- Finalização do temporizador
- Consulta do status atual do temporizador

### RF05 - Seção "o que mudou"

A API deve permitir registrar mudanças na rotina diária.

Cada mudança deve conter:

- Identificador único
- Data
- Descrição da mudança
- Atividades impactadas
- Nível de relevância
- Mensagem curta para exibição ao usuário

### RF06 - Gatilhos contextuais

A API deve permitir definir e aplicar gatilhos condicionais simples.

Exemplos de gatilhos:

- Se o dia da semana for terça-feira, mostrar checklist de saída para terapia.
- Se houver atividade escolar, mostrar cartões de mochila, lanche e uniforme.
- Se houver mudança na rotina, destacar a seção "o que mudou".

### RF07 - Apoio assistido por IA

A API deve prever integração com IA para apoiar:

- Sugestão de checklists
- Sugestão de cartões visuais
- Sugestão de adaptações para mudanças inesperadas
- Geração de mensagens curtas e objetivas sobre mudanças na rotina

No MVP, a IA pode ser representada por uma camada de serviço isolada, mesmo que inicialmente use respostas simuladas.

### RF08 - Healthcheck

A API deve expor um endpoint de verificação de saúde.

Endpoint mínimo:

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

## Requisitos Não Funcionais

### RNF01 - Stack

A API deve ser desenvolvida em Python com FastAPI.

### RNF02 - Organização do código

O projeto deve manter separação clara entre:

- Rotas
- Contratos
- Modelos
- Serviços
- Regras de negócio
- Testes

### RNF03 - Tipagem

O código deve usar tipagem explícita sempre que possível.

### RNF04 - Validação de dados

Entradas e saídas da API devem ser validadas com contratos Pydantic.

### RNF05 - Documentação

A API deve manter documentação interativa disponível via OpenAPI/Swagger.

### RNF06 - Testabilidade

O MVP deve permitir testes automatizados para endpoints, regras de negócio e serviços principais.

### RNF07 - Baixo acoplamento

A camada de IA deve ser desacoplada das rotas e das regras centrais, permitindo troca futura do provedor.

### RNF08 - Segurança básica

O MVP deve evitar exposição de dados sensíveis em logs, respostas de erro e configurações versionadas.

### RNF09 - Configuração por ambiente

Configurações sensíveis ou variáveis por ambiente devem ser carregadas por variáveis de ambiente.

### RNF10 - Execução local simples

O projeto deve poder ser executado localmente com ambiente virtual e dependências instaladas via `requirements.txt`.

## Fora de Escopo

- Interface web ou aplicativo mobile.
- Autenticação e autorização de usuários.
- Controle multiusuário ou perfis familiares.
- Persistência definitiva em banco de dados relacional.
- Painel administrativo.
- Notificações push, SMS, e-mail ou WhatsApp.
- Integração real obrigatória com provedor de IA no primeiro incremento.
- Upload e armazenamento de imagens.
- Geração automática de imagens para cartões visuais.
- Sincronização com calendários externos.
- Deploy em ambiente de produção.
- Observabilidade avançada com métricas, tracing e alertas.
- Motor complexo de regras com linguagem própria.
- Personalização clínica ou terapêutica avançada.
