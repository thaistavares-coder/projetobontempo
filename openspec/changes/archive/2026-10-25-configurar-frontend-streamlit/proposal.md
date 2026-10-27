## Why

O projeto já definiu Python e Streamlit como tecnologias do frontend, mas o repositório ainda não possui estrutura ou especificação para a interface web. Esta mudança estabelece uma base mínima e coerente para iniciar o frontend sem alterar o backend Xano nem antecipar funcionalidades de agenda.

## What Changes

- Definir a estrutura inicial de uma aplicação web em Python com Streamlit.
- Especificar navegação entre Início, Pacientes e Profissionais.
- Documentar que o frontend consome as APIs HTTP existentes do Xano e não acessa o banco diretamente.
- Registrar como pendências a URL base das APIs, os requisitos de autenticação e a análise do valor aparentemente sensível no repositório.
- Atualizar `AGENTS.md` e `docs/project-overview.md` para documentar Streamlit.
- Manter fora do escopo agendamentos, disponibilidades, alterações em Xano e mudanças nas especificações consolidadas de pacientes e profissionais.

## Capabilities

### New Capabilities

- `interface-web`: estrutura inicial da interface Streamlit, navegação principal e limites de integração com as APIs HTTP existentes.

### Modified Capabilities

Nenhuma. As especificações existentes de pacientes e profissionais não terão seus requisitos alterados.

## Impact

- Planejamento da futura pasta `frontend/`, com ponto de entrada, páginas e módulo compartilhado de acesso HTTP/configuração.
- Documentação do projeto em `AGENTS.md` e `docs/project-overview.md`.
- APIs existentes em `xano/api/pacientes/` e `xano/api/profissionais/` são referências para integração futura; não serão modificadas.
- Dependências Python e configuração da URL base serão definidas na implementação, após confirmação do ambiente e dos requisitos de autenticação.
