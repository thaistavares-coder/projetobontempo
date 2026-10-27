## Why

A estrutura atual permite navegar entre Início, Pacientes e Profissionais, mas ainda não apresenta uma identidade visual consistente nem organiza a informação de forma suficientemente clara. Esta mudança aprimora a experiência visual sem ampliar as funcionalidades do sistema ou depender de dados e serviços externos.

## What Changes

- Aplicar uma apresentação visual profissional e consistente às três páginas existentes, priorizando azul, verde-água, fundo claro, navegação lateral e componentes nativos do Streamlit.
- Apresentar na página Início uma breve descrição do sistema e cards informativos sem dados inventados.
- Organizar as páginas Pacientes e Profissionais com título de módulo e mensagem de que suas funcionalidades serão implementadas futuramente.
- Manter a navegação restrita a Início, Pacientes e Profissionais.
- Preservar a execução sem login, chamadas HTTP ao Xano, dados fictícios de pacientes ou profissionais, CRUD, agendamentos ou alterações no backend.

## Capabilities

### New Capabilities

- `interface-web`: apresentação visual consistente e conteúdo estático das três páginas existentes do frontend Streamlit.

### Modified Capabilities

Nenhuma.

## Impact

- Código afetado: `frontend/app.py` e as páginas existentes em `frontend/pages/`.
- APIs, backend e dependências: sem alterações previstas.
- A navegação continua sendo feita pelo Streamlit; a mudança não adiciona páginas nem integrações.
