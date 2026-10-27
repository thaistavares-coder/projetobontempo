## Why

As páginas Streamlit de Pacientes e Profissionais ainda persistem no SQLite, enquanto o cliente Xano existente atende somente listagens GET e não é utilizado pelas páginas. Esta mudança prepara a migração dessas duas capacidades para o Xano com CRUD por APIs HTTP, preservando registros existentes e sem assumir que definições locais provem quais recursos estão publicados.

## What Changes

- Reconciliar em modo somente leitura as tabelas, campos, validações, permissões e endpoints publicados de Pacientes e Profissionais com os arquivos XanoScript locais antes de decidir quais endpoints realmente precisam ser criados ou corrigidos.
- Completar as operações HTTP de criar, listar, consultar por ID, editar e remover pacientes e profissionais, respeitando os contratos existentes e sem alterar autenticação, permissões, credenciais ou dados preexistentes.
- Criar um serviço Python tipado e reutilizável para chamadas HTTP, configuração externa, timeout, validação de respostas e tratamento explícito de erros; manter a integração real desabilitada até a configuração e a autorização operacional necessárias.
- Conectar as páginas Streamlit de Pacientes e Profissionais ao serviço Xano, incluindo cadastro, edição, listagem e exclusão com confirmação explícita, sem acesso direto ao banco Xano.
- Testar contratos e fluxos com respostas HTTP simuladas e dados sintéticos; qualquer teste de integração no Xano deverá ser autorizado separadamente, usar registros sintéticos criados para o teste e não alterar ou remover registros preexistentes.
- Preservar os contratos atuais de campos básicos e a especialidade textual legada de Profissionais; não introduzir nesta mudança o catálogo relacional, vínculos N:N ou consultas.
- Tratar SQLite exclusivamente como persistência legada temporária: deixar de usá-lo em Pacientes e Profissionais nesta mudança, migrar depois Especialidades e Consultas para APIs Xano em Changes subsequentes e então remover o serviço/dependência SQLite da aplicação. Não criar uma arquitetura permanente com dois bancos; preservar o arquivo SQLite local até uma autorização e um plano de retenção/migração próprios.
- Bloquear alterações de schema e publicação de endpoints até revisão do inventário remoto e autorização explícita para cada operação no ambiente `v1` live; não usar publicação ampla do workspace.

**Fora do escopo:** criação de tabelas ou migração de dados; alteração de autenticação, permissões ou credenciais; CRUD de Especialidades, vínculos N:N ou Consultas; remoção física do serviço e dependência SQLite antes que as páginas restantes sejam migradas em Changes subsequentes; testes destrutivos sobre registros preexistentes; publicação ou alteração remota nesta etapa de planejamento.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `pacientes`: exigir operações de CRUD consumidas pelo Streamlit através de APIs Xano confirmadas, com validação, erros explícitos e proteção contra exclusão acidental ou testes sobre registros existentes.
- `profissionais`: exigir operações de CRUD consumidas pelo Streamlit através de APIs Xano confirmadas, preservando o campo textual de especialidade e sem introduzir a relação N:N nesta mudança.
- `interface-web`: permitir que as páginas Pacientes e Profissionais usem o serviço HTTP Xano configurado externamente, com estados de erro e confirmação de exclusão; manter as demais páginas locais durante a transição.

## Impact

- Frontend: `frontend/services/listagens.py` e novos serviços HTTP compartilhados; `frontend/pages/1_Pacientes.py` e `frontend/pages/2_Profissionais.py`; testes e documentação do frontend.
- XanoScript local: revisar os schemas e os arquivos CRUD existentes em `xano/table/` e `xano/api/`, alterando somente definições justificadas pela comparação remota e após autorização. Os arquivos locais não confirmam publicação.
- Xano remoto: workspace `153318`, cuja única branch confirmada é `v1` live e cujo metadado consultado indica `allow_push: false`. Nenhuma alteração remota está autorizada por esta proposta; publicação seletiva depende de verificar as restrições da plataforma e receber autorização explícita.
- Dados: não migrar, substituir, limpar ou remover dados existentes. Testes automatizados usam mocks; eventuais testes remotos futuros usam somente registros sintéticos criados para esse fim.
- SQLite: é legado transitório, não parte da arquitetura final. Especialidades e Consultas ainda dependem dele e serão migradas em Changes subsequentes; após essa migração, outra etapa removerá o serviço/dependência SQLite. O arquivo local permanece preservado até autorização e decisão específica sobre retenção/importação.
- Segurança: URL e eventuais credenciais permanecem em configuração externa; não expor segredos no repositório, alterar permissões ou presumir que os dados remotos sejam fictícios.
