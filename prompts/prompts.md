Prompt 1
Contexto: Estou iniciando uma API Python com FastAPI em um repositorio de produto.
Objetivo: Gere um arquivo .gitignore para Python, ambiente virtual, cache de testes e
configuracoes locais do editor.
Estilo: Organize por secoes com comentarios.
Resposta: Forneca apenas o conteudo do arquivo .gitignore.
tive que fazer :
- ok, mas quero que vc crie .gitignore e pode tambem criar o ambiente virtual no .venv
- Esse projeto ainda não está versionado. Inicie o git pra mim


Prompt 2 - README inicial
Contexto: MVP de micro-API para Agenda diária com cartões visuais, temporizadores, checklist, seção “o que mudou” e gatilhos do tipo “se terça = terapia, mostrar checklist de saída” assistida por IA.
Objetivo: Escrever um README inicial com objetivo, stack, como rodar localmente e roadmap de
releases.
Estilo: Markdown simples, direto e profissional.
Resposta: Forneca o README completo.

Prompt 3 - Endpoint de healthcheck
Contexto: Projeto em Python 3.11 com FastAPI.
Objetivo: Criar app/main.py com uma instancia FastAPI e endpoint GET /health retornando status
ok e timestamp.
Estilo: Tipagem e codigo limpo.
Resposta: Forneca apenas o codigo de app/main.py.

Prompt 4 - Arquivo Requirements
Preciso de um arquivo de requirements para ter os pacotes necessdrios para esse projeto, pode inclusive utilizar o ambiente virutal criado e instalar os pacotes necessdrios

faltou ppytest

Prompt 5 - Revisao critica
Analise o codigo gerado para app/main.py e responda:
1) Quais riscos tecnicos existem?
2) 0 que pode quebrar em producao?
3) Quais testes minimos devo criar agora?
Resposta curta em checklist.

Prompt 6 - Mensagem de commit
Contexto: Adicione estrutura inicial, README, .gitignore e endpoint /health. Veja também outras alteracões que nao estado aqui listadas.
Objetivo: Gerar uma mensagem de commit no padrao Conventional Commits.
Apenas uma linha de commit.

Prompt 7 -
Contexto: MVP de micro-API para Agenda diária com cartões visuais, temporizadores,checklist, seção “o que mudou” e gatilhos do tipo “se terça = terapia, mostrar checklist de saída” assistida por IA.
Objetivo: Gerar documento de escopo com objetivo, requisitos funcionais, nao funcionais e fora de escopo.
Estilo: Linguagem tecnica, direta, em Markdown.
Resposta: Forneca o conteudo completo de docs/escopo-mvp.md.

Prompt 8 - Backlog Releases
Contexto: 0 produto sera entregue em 3 releases: core, qualidade e entrega final.
Objetivo: Criar backlog minimo com IDs RF/RT e criterios de aceite.
Estilo: Checklist Markdown.
Resposta: Conteudo de docs/backlog.md.

Prompt 9 - Gerar Mermaid
Contexto: FastAPI com camadas API, Service, Repository e componente PriorityAdvisor.
Objetivo: Gerar diagrama Mermaid de componentes e fluxo de dados.
Estilo: Simples, legivel e versionavel.
Resposta: Apenas bloco Mermaid com o arquivo no repositorio.

Prompt 10 - COmmit
Contexto: Adicionei docs/escopo-mvp.md, docs/diagrama-componentes.md e docs/backlog.md.
Objetivo: Sugerir 3 mensagens de commit no padrao Conventional Commits.
Resposta: Apenas as 3 linhas de commit e faça os commits para mim.

Prompt 11 - Revisão do Planejamento
Analise este escopo e backlog e responda:
1) 0 que esta grande demais para a release inicial?
2) 0 que esta faltando para testabilidade?
3) Quais 3 riscos tecnicos devo mitigar antes da implementacao?
Resposta em bullets curtos.

Prompt 11 - Modelo Pydantic
Contexto: API em FastAPI para o MVP de Agenda Diária Assistida por IA, com cartões visuais, checklists, temporizadores, seção “o que mudou” e gatilhos contextuais. Conforme o README, a API deve representar atividades da rotina diária e preparar a base para endpoints de agenda.
Objetivo: Gerar modelos Pydantic ActivityCreate, ActivityUpdate e ActivityOut para representar uma atividade da agenda diária. Os modelos devem incluir tipagem e validações para os campos: id UUID opcional na criação e obrigatório na saída, title string obrigatória com mínimo de 3 e máximo de 100 caracteres, description string opcional, scheduled_time datetime opcional, period string opcional, status com valores pending, in_progress, done e canceled, visual_card_ids lista de UUIDs, checklist_id UUID opcional, timer_id UUID opcional, has_changes booleano com padrão False, created_at datetime e updated_at datetime opcional.
Estilo: Pydantic v2, código limpo, tipagem estática, validações com Field e docstrings curtas nos modelos.
Resposta: Apenas código de app/models/activity.py.

Prompt 12 - Repositório Inicial
Contexto: Preciso de persistencia inicial enxuta para viabilizar a primeira release.
Objetivo: Criar ActivityRepository em memoria com create, list, get_by_id, update e delete.
Estilo: Python tipado, sem dependencias externas.
Resposta: Codigo completo de app/repositories/activity_repository.py.

Prompt 13 - Service com Regra de Prioridade 
Contexto: A prioridade da activity pode ser sugerida automaticamente.
Objetivo: Criar ActivityService que use ActivityRepository e PriorityAdvisor.
Estilo: Separar regra de negocio da camada de API.
Resposta: Codigo de app/services/activity_service.py.


Prompt 14 - PriorityAdvisdor com fallback
Contexto: Quero rodar sem custo de API quando nao houver chave.
Objetivo: Implementar PriorityAdvisor com heuristica local e chamada opcional a LLM
quando OPENAI_API_KEY existir.
Estilo: Falha segura, timeout e fallback obrigatorio.
Resposta: Codigo de app/services/priority_advisor.py.

Prompt 15 - CRUD Rotas
Contexto: FastAPI com ActivityService pronto.
Objetivo: Criar rotas POST/GET/PUT/DELETE para ativities com status HTTP corretos e tratamento de 404.
Estilo: Router separado em app/api/activity_routes.py.
Resposta: Apenas o codigo do arquivo.

Prompt 16 - Revisao tecnica
Revise os arquivos do core da API e responda:
1) Quais pontos de acoplamento estao altos?
2) Onde faltam validacoes?
3) Quais 5 testes devo priorizar na proxima release?
Resposta em checklist.

prompt 17 - Commits
Existem muitos diffs e muitas camadas da aplicacao ainda sem commit. Utilize conventional commits para cada uma das camadas em separado e faca os commits para mim.


Prompt 18 - Testes do service
Contexto: Tenho ActivityService com CRUD de atividades.
Objetivo: Gerar suite Pytest cobrindo criacao, listagem, atualizacao, exclusao e caso de erro por ID inexistente.
Estilo: Testes claros, nomes descritivos e fixtures simples.
Resposta: Codigo completo de tests/test_activity_service.py.

Prompt 19 = Test PriorityAdvisor
Contexto: PriorityAdvisor possui heuristica local e fallback quando chamada externa
falha.
Objetivo: Gerar testes para os tres niveis de prioridade e para fallback.
Estilo: Usar monkeypatch quando necessario.
Resposta: Codigo de tests/test_priority_advisor.py.

Prompt 20 - Testes de API at
Contexto: API FastAPI com endpoints CRUD de /activities.
Objetivo: Criar testes de rota com TestClient para status 201, 200, 204 e 404.
Estilo: Isolar dependencia de repositorio para evitar estado global entre testes.
Resposta: Codigo de tests/test_activity_routes.py.

Prompt 21 - Refatoracao DRY/SRP =
Analise os arquivos app/services/task_service.py e app/repositories/task_repository.py.
Objetivo: Sugerir refatoracao com foco em DRY e SRP sem mudar comportamento externo.
Resposta: 1) lista de mudancas propostas 2) patch sugerido por arquivo.

Prompt 22 - Readme final tecnico
Contexto: MVP de micro-API de tarefas com prioridade assistida por IA.
Objetivo: Gerar README completo com instalacao, execucao, testes, arquitetura, uso da IA, limitacoes e proximos passos.
Estilo: Markdown profissional e objetivo.
Resposta: README inteiro.

Prompt 23 - Revisao final de qualidade
Com base no codigo e nos testes atuais, gere um checklist com:
- Riscos tecnicos restantes
- Gaps de cobertura de teste
- Melhorias prioritarias para a proxima release
Resposta em bullets curtos.

0k, agora que temos bastantes testes podemos executar para verificar se esta tudo correto. Avalie para mim

Pode fazer os commits com as devidas mensagens

Eu queria ver a api funcionando. Rode ela pra mim e mostre alguns casos de cliente criando task e listando task

Entao quer dizer que ainda faltavam cobertura de testes porque alguns endpoints ainda nao haviam sido testados, avalie
como aumentar a cobertura desses testes

Pode fazzer os commit


Prompt 24 - Makefile
Contexto: Projeto FastAPI com comandos de instalar dependencias, executar API e rodar testes.
Objetivo: Gerar Makefile com targets install, run e test.
Estilo: Simples e portavel.
Resposta: Conteudo completo de Makefile.

Prompt 25 - .env.example 
Contexto: 0 projeto usa integracao opcional de LLM.
Objetivo: Criar arquivo .env.example com variaveis necessarias e valores placeholder seguros.
Estilo: Minimalista.
Resposta: Apenas conteudo do arquivo.

Prompt 26 - Revisao de README
Analise meu README e responda:
1) 0 que falta para ser reproduzivel em maquina limpa?
2) Quais secoes estao fracas para onboarding tecnico?
3) Como melhorar a secao de uso da IA?
Resposta em checklist objetivo)

0k, atualize o readme para mim para que tenha essas correcões

Faça os comits em das alterações em separados
Prompt 27 - Checklist de release
Contexto: Vou publicar a versao v1.0.@ no GitHub.
Objetivo: Gerar checklist final com itens tecnicos e de documentacao para release.~
Estilo: Checkbox Markdown.
Resposta: Lista completa.