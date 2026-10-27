## Context

A aplicação Streamlit atual já possui a navegação entre Início, Pacientes e Profissionais. As páginas exibem conteúdo mínimo e não dependem do Xano. Consulte `proposal.md` e `specs/interface-web/spec.md` para motivação e comportamento esperado.

## Goals / Non-Goals

**Goals:**

- Dar unidade visual às três páginas sem mudar sua estrutura de navegação.
- Usar componentes nativos do Streamlit para manter a interface simples e acessível.
- Tornar o conteúdo da página Início informativo sem apresentar dados de domínio inexistentes.

**Non-Goals:**

- Criar fluxos de autenticação, integrações ou persistência.
- Construir módulos funcionais de pacientes ou profissionais.
- Criar páginas, operações de CRUD, agendamentos ou disponibilidades.

## Decisions

- Manter o ponto de entrada e as duas páginas existentes como as únicas páginas da aplicação; preservar a navegação lateral já utilizada pelo Streamlit. Isso evita introduzir novas estruturas de navegação ou páginas duplicadas.
- Definir a identidade visual em azul e verde-água, com fundo claro, por meio dos recursos de tema suportados pelo Streamlit. Usar componentes nativos, como colunas e contêineres com borda, para organizar os cards e o conteúdo sem depender de HTML/CSS customizado.
- Construir os cards da página Início com descrições estáticas sobre o sistema e os módulos, sem números, registros ou exemplos de pacientes e profissionais. Assim, os cards comunicam a finalidade do sistema sem simular dados.
- Manter nas páginas Pacientes e Profissionais apenas o título do módulo e a mensagem de implementação futura, preservando sua natureza informativa.
- Não incluir dependências, configuração de API ou alterações no Xano; a mudança permanece isolada à apresentação do frontend.

## Risks / Trade-offs

- [Ajustes visuais podem variar entre versões ou temas do Streamlit] → Usar componentes e opções de tema suportados pela versão já declarada no projeto e validar a aplicação localmente.
- [Cards podem ser confundidos com indicadores de dados reais] → Limitar seu conteúdo a descrições institucionais estáticas, sem contagens, exemplos ou registros.
