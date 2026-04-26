# Backlog do MVP

## Release 1 - Núcleo

- [ ] **RF01 - Healthcheck da API**
  - Critérios de aceite:
    - [ ] Deve existir endpoint `GET /health`.
    - [ ] Deve retornar HTTP `200`.
    - [ ] Deve retornar `status` com valor `ok`.
    - [ ] Deve retornar `timestamp` em formato ISO.

- [ ] **RF02 - Consulta da agenda diária**
  - Critérios de aceite:
    - [ ] Deve existir endpoint para consultar a agenda por data.
    - [ ] A resposta deve listar as atividades do dia.
    - [ ] Cada atividade deve conter identificador, título, horário ou período e status.
    - [ ] Quando não houver atividades, deve retornar lista vazia.

- [ ] **RF03 - Cartões visuais**
  - Critérios de aceite:
    - [ ] Deve ser possível cadastrar cartão visual.
    - [ ] Deve ser possível listar cartões visuais.
    - [ ] Cada cartão deve conter identificador, título, tipo e referência visual.
    - [ ] Cartões devem poder ser associados a atividades.

- [ ] **RF04 - Checklists por atividade**
  - Critérios de aceite:
    - [ ] Deve ser possível criar checklist vinculado a uma atividade.
    - [ ] Deve ser possível listar itens do checklist.
    - [ ] Cada item deve possuir descrição e status de conclusão.
    - [ ] Deve ser possível marcar item como concluído.

- [ ] **RT01 - Estrutura inicial do projeto**
  - Critérios de aceite:
    - [ ] O projeto deve manter diretórios separados para rotas, contratos, serviços e testes.
    - [ ] A aplicação FastAPI deve iniciar a partir de `app/main.py`.
    - [ ] As dependências devem estar declaradas em `requirements.txt`.
    - [ ] Arquivos locais e ambiente virtual devem estar ignorados no `.gitignore`.

## Release 2 - Qualidade

- [ ] **RF05 - Temporizadores**
  - Critérios de aceite:
    - [ ] Deve ser possível associar duração estimada a uma atividade.
    - [ ] Deve ser possível iniciar temporizador.
    - [ ] Deve ser possível pausar temporizador.
    - [ ] Deve ser possível finalizar temporizador.
    - [ ] Deve ser possível consultar o status atual do temporizador.

- [ ] **RF06 - Seção "o que mudou"**
  - Critérios de aceite:
    - [ ] Deve ser possível registrar mudança na rotina do dia.
    - [ ] Cada mudança deve conter data, descrição e nível de relevância.
    - [ ] Mudanças devem poder ser associadas a atividades impactadas.
    - [ ] A agenda diária deve indicar quando houver mudanças relevantes.

- [ ] **RF07 - Gatilhos contextuais simples**
  - Critérios de aceite:
    - [ ] Deve ser possível definir gatilho por dia da semana.
    - [ ] Deve ser possível definir gatilho por atividade.
    - [ ] Deve ser possível aplicar gatilho na montagem da agenda diária.
    - [ ] O caso "terça-feira com terapia" deve exibir checklist de saída.

- [ ] **RT02 - Testes automatizados mínimos**
  - Critérios de aceite:
    - [ ] Deve existir teste para `GET /health`.
    - [ ] Deve existir teste para consulta de agenda diária.
    - [ ] Deve existir teste para validação de contrato dos principais endpoints.
    - [ ] Os testes devem rodar com `pytest`.

- [ ] **RT03 - Validação e contratos**
  - Critérios de aceite:
    - [ ] Entradas da API devem ser validadas com contratos Pydantic.
    - [ ] Respostas principais devem possuir modelos de saída definidos.
    - [ ] Erros de validação devem retornar resposta padronizada do FastAPI.
    - [ ] A documentação OpenAPI deve carregar sem erro.

## Release 3 - Entrega final

- [ ] **RF08 - Apoio assistido por IA**
  - Critérios de aceite:
    - [ ] Deve existir serviço isolado para sugestões assistidas por IA.
    - [ ] Deve ser possível solicitar sugestão de checklist por contexto.
    - [ ] Deve ser possível solicitar sugestão de adaptação para mudança na rotina.
    - [ ] O serviço deve permitir uso inicial com resposta simulada.

- [ ] **RF09 - Consolidação da agenda diária**
  - Critérios de aceite:
    - [ ] A agenda deve consolidar atividades, cartões, checklists, temporizadores e mudanças.
    - [ ] Gatilhos contextuais devem ser aplicados na resposta consolidada.
    - [ ] A resposta deve estar pronta para consumo por interface visual futura.
    - [ ] Campos opcionais devem ser retornados de forma consistente.

- [ ] **RT04 - Configuração por ambiente**
  - Critérios de aceite:
    - [ ] Configurações variáveis devem ser lidas por variáveis de ambiente.
    - [ ] Valores sensíveis não devem ser versionados.
    - [ ] Deve existir exemplo documentado de configuração local.
    - [ ] A aplicação deve iniciar sem depender de segredos reais no ambiente local.

- [ ] **RT05 - Documentação de entrega**
  - Critérios de aceite:
    - [ ] O README deve conter instruções atualizadas para rodar o projeto.
    - [ ] O escopo do MVP deve estar documentado em `docs/escopo-mvp.md`.
    - [ ] O backlog deve estar documentado em `docs/backlog.md`.
    - [ ] A documentação deve indicar limitações e itens fora de escopo.

- [ ] **RT06 - Preparação para release**
  - Critérios de aceite:
    - [ ] Todos os testes automatizados devem passar.
    - [ ] A API deve iniciar localmente com `uvicorn app.main:app --reload`.
    - [ ] A documentação interativa deve estar disponível em `/docs`.
    - [ ] Deve existir mensagem de commit seguindo Conventional Commits para a entrega.
