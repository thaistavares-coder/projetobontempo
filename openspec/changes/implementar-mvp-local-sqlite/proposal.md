## Why

O MVP local do consultório já está implementado e validado, mas as Changes ativas descrevem outras etapas e não registram o comportamento demonstrável do Streamlit com persistência SQLite. Esta Change documenta o que existe e suas limitações, para que a apresentação e a evolução do projeto partam de um escopo fiel sem confundir a demonstração local com integração ao Xano.

## What Changes

- Registrar a aplicação Streamlit local com navegação para Início, Pacientes, Profissionais, Especialidades e Consultas.
- Documentar persistência SQLite local, cadastros e listagens de pacientes, profissionais e especialidades, incluindo vínculo N:N entre profissionais e especialidades.
- Documentar criação e listagem de consultas, os status disponíveis, a atualização de status e a prevenção de conflitos de horário para consultas que ocupam horário.
- Registrar a carga explícita de dados fictícios e os ajustes visuais de contraste dos formulários.
- Explicitar que este modo não possui autenticação, prontuários, disponibilidade profissional nem integração ativa com Xano; o cliente GET já existente não é usado pelas páginas deste MVP.
- Manter inalterados o código funcional, o Xano, seus endpoints e as três Changes OpenSpec existentes.

## Capabilities

### New Capabilities

- `mvp-local-sqlite`: comportamento e limites da demonstração local do consultório com Streamlit e SQLite.

### Modified Capabilities

Nenhuma. Esta Change registra o modo de demonstração local sem reescrever os contratos das capacidades e Changes existentes do Xano.

## Impact

- Implementação existente: `frontend/app.py`, `frontend/ui.py`, páginas Streamlit, `frontend/services/database.py`, testes e configuração de ignore/documentação do frontend.
- Persistência: arquivo SQLite local em `frontend/data/bontempo_demo.sqlite3`, excluído do Git pelo `.gitignore`.
- Nenhum endpoint, tabela, configuração ou dado do Xano será alterado; nenhuma requisição ao Xano é feita por este modo local.
- Esta Change é documental e retrospectiva: não autoriza executar `apply`, `archive`, `git add`, commit, push ou deploy.
