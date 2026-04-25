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
