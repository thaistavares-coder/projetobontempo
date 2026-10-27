## Why

A interface atual já apresenta identidade visual e navegação, mas ainda não oferece o nível de hierarquia e acabamento adequado para uma apresentação acadêmica de um sistema administrativo de consultório. Esta mudança aprimora visualmente as três páginas existentes e representa os módulos ainda não integrados por estados vazios explícitos, sem sugerir operações concluídas ou dados reais.

## What Changes

- Refinar a identidade visual Bontempo com cabeçalhos, ícones, tipografia e espaçamentos consistentes nas páginas Início, Pacientes e Profissionais.
- Apresentar na página Início cards de navegação para Pacientes e Profissionais e uma indicação discreta de Agenda futura, sem criar página ou indicador numérico.
- Apresentar em Pacientes e Profissionais cabeçalho, descrição, busca e botão de criação desabilitados e uma tabela vazia com colunas compatíveis com os campos definidos nas especificações.
- Informar explicitamente que a integração com Xano ainda não está disponível.
- Manter a navegação atual e usar componentes nativos do Streamlit com CSS pontual, sem adicionar dependências.

Ficam fora do escopo: login/autenticação, chamadas HTTP, dados fictícios, operações CRUD ou persistidas, agendamentos, disponibilidades, novas páginas e alterações em backend, tabelas ou XanoScript.

## Capabilities

### New Capabilities

- `interface-web`: apresentação visual das páginas existentes e representação explícita de módulos sem integração, sem introduzir comportamento de negócio.

### Modified Capabilities

Nenhuma.

## Impact

- Código afetado: `frontend/app.py` e as páginas existentes em `frontend/pages/`.
- As especificações de pacientes e profissionais são usadas somente para manter compatíveis os nomes dos campos apresentados; seus requisitos de backend não mudam.
- APIs, backend, tabelas, XanoScript e dependências permanecem inalterados.
