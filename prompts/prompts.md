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