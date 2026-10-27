## Why

Esta Change especificou a primeira integração de leitura: as páginas Pacientes e Profissionais passaram a listar dados por GET do Xano. A Change `crud-pacientes-profissionais-xano-streamlit` evoluiu esse trabalho para o CRUD completo desses dois módulos. Esta Change permanece como registro da etapa GET inicial; suas limitações de escopo não proíbem as operações posteriormente especificadas pela Change CRUD.

## What Changes

- Integrar inicialmente as páginas existentes de Pacientes e Profissionais às respectivas operações HTTP GET de listagem; a evolução para CRUD é especificada pela Change `crud-pacientes-profissionais-xano-streamlit`.
- Centralizar configuração, transporte HTTP, timeout e validação de resposta em um cliente Python reutilizável, com URLs completas fornecidas externamente por variável de ambiente.
- Substituir as tabelas vazias por registros realmente recebidos, mantendo as colunas e o layout atuais; apresentar estados explícitos de lista vazia, configuração ausente e falha de integração.
- Evitar chamadas repetidas durante reruns da interface com cache de curta duração e atualização manual.
- Nesta etapa inicial, manter busca e escrita fora do escopo. A Change CRUD posterior passa a definir cadastro, edição e exclusão para Pacientes e Profissionais; login e gerenciamento de usuários continuam fora do escopo.
- Manter `especialidade` como texto da resposta atual de Profissionais, sem introduzir relacionamento com catálogo.
- Planejar testes automatizados com respostas HTTP simuladas para sucesso, lista vazia, erro HTTP, timeout, falha de conexão e JSON/formato inesperado.
- Manter as chamadas reais desabilitadas por padrão e exigir habilitação externa explícita somente após confirmação de dados exclusivamente fictícios, acesso adequadamente restrito e autorização do grupo; os GETs já testados sem credenciais não são evidência de segurança.

**Escopo desta etapa inicial:** somente listagens GET. As operações POST, PATCH e DELETE de Pacientes e Profissionais foram posteriormente especificadas na Change `crud-pacientes-profissionais-xano-streamlit`, e não são uma proibição para a implementação combinada. Permanecem fora do escopo alteração de autenticação/permissões, login, consultas clínicas, prontuários, Especialidades como módulo, relacionamento N e outras capacidades da Change `revisar-escopo-modelo-clinica`, bem como mudanças nas cardinalidades ou no modelo de dados.

## Capabilities

### New Capabilities

Nenhuma. O trabalho integra listagens nas capacidades de interface, pacientes e profissionais já especificadas; não cria capacidade clínica nova.

### Modified Capabilities

- `interface-web`: substituir o contrato de páginas somente informativas/tabelas vazias pela apresentação das listagens GET e seus estados de resposta, preservando navegação, identidade visual e ausência de operações de escrita.
- `pacientes`: especificar consumo GET da listagem existente, campos exibidos, lista vazia e erros de leitura.
- `profissionais`: especificar consumo GET da listagem existente, incluindo `especialidade` textual, lista vazia e erros de leitura.

## Impact

- A camada GET desta etapa mantém sua trava `XANO_LISTAGENS_ENABLED`, desabilitada por padrão. A integração atual das páginas é definida pela Change CRUD, incluindo sua própria configuração e trava. A tarefa de confirmar segurança dos dados e endpoints permanece pendente; uma resposta GET bem-sucedida não é evidência suficiente.
- Futura implementação: `frontend/pages/1_Pacientes.py`, `frontend/pages/2_Profissionais.py`, novo módulo reutilizável sob `frontend/services/`, `frontend/requirements.txt` e `frontend/README.md`; avaliar ajuste mínimo em `frontend/app.py` ou `frontend/ui.py` somente se necessário para consistência visual.
- Configuração desta etapa: duas variáveis externas com URLs completas dos GETs de Pacientes e Profissionais. A Change CRUD posterior define a configuração usada pelas páginas integradas atualmente. Nenhum token, segredo ou URL operacional deve ser incluído em arquivos versionados.
- Dependência prevista para a implementação: `requests` declarada diretamente caso seja escolhida como cliente HTTP; testes usando biblioteca padrão para simular respostas, sem dados reais.
- Xano: somente os endpoints GET existentes e informados pelo grupo são consumidores; os arquivos locais indicam rotas e projeções de campos equivalentes, mas não comprovam integralmente o ambiente publicado.
- A Change `revisar-escopo-modelo-clinica` foi consultada somente para delimitar conflitos: não será alterada, aplicada, arquivada nem será dependência desta Change. A leitura se limita às listagens atuais de Pacientes e Profissionais, mantendo especialidade textual e adiando os demais módulos.
