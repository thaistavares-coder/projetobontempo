## Why

O domínio e as especificações atuais descrevem pacientes, profissionais e agenda, mas o Xano local contém somente tabelas de usuário, paciente e profissional; ainda não há estrutura para especialidades, consultas ou prontuários. Antes de integrar Streamlit e Xano ou tratar dados clínicos, o grupo precisa reconciliar o escopo aprovado, as lacunas observadas e as cardinalidades ainda incertas, incluindo os riscos de privacidade sem login.

## What Changes

- Registrar como escopo aprovado cinco módulos funcionais — Pacientes, Profissionais exclusivamente médicos, Especialidades médicas, Consultas e Prontuários — mantendo Início como página de apresentação e navegação, sem implementar novas telas.
- Especificar as decisões aprovadas sobre prontuário e registro de atendimento, mantendo diagnóstico, anotações clínicas e conduta no registro, e não duplicados em Consulta.
- Registrar como aprovada a relação N:N entre MÉDICO e ESPECIALIDADE, permitindo zero vínculos durante a transição e exigindo vínculo válido para agendar uma consulta; manter pendentes as demais decisões de cardinalidade, integridade, status e exclusão que o contexto não resolva.
- Comparar tabelas, APIs e especificações locais com o modelo proposto; identificar endpoints de usuário e dependências de autenticação sem presumir que os arquivos locais representem a configuração publicada.
- Registrar riscos de confidencialidade e critérios de segurança para dados clínicos sem introduzir login, gerenciamento de usuários/papéis ou integração nesta Change.
- Após a aprovação das decisões de domínio, atualizar `docs/project-overview.md` e `docs/domain-model.md` para distinguir escopo aprovado de capacidades ainda não implementadas, e propor a implementação em Changes pequenas.

**Fora do escopo:** modificar, criar ou excluir tabelas, registros ou endpoints; alterar código Python/XanoScript; implementar autenticação, CRUD clínico ou integração Streamlit–Xano; decidir silenciosamente cardinalidades pendentes; usar dados reais de pacientes; executar archive, commit ou push.

## Capabilities

### New Capabilities

- `modelo-clinico`: registrar as decisões conceituais aprovadas, os pontos de modelagem que precisam de confirmação e os critérios de integridade e privacidade que devem anteceder a implementação clínica.

### Modified Capabilities

- `pacientes`: explicitar a relação futura com prontuário e impedir que a regra de exclusão atual seja interpretada como autorização para deixar dados clínicos órfãos.
- `profissionais`: restringir o escopo futuro a médicos e registrar a relação N:N aprovada com especialidades, sem exigir vínculo antes da transição e exigindo-o para consultas.
- `interface-web`: alinhar o escopo-alvo de navegação às cinco áreas funcionais e à página Início, preservando o estado atual sem integração HTTP nesta Change.

## Impact

- Artefatos OpenSpec: nova delta `modelo-clinico` e deltas para `pacientes`, `profissionais` e `interface-web`.
- Referências de implementação analisadas: `xano/table/user.xs`, `paciente.xs`, `profissional.xs`; grupos e endpoints locais de autenticação/usuário, pacientes e profissionais; frontend Streamlit atual.
- Documentação de domínio e visão geral: atualizar somente após as decisões pendentes receberem aprovação explícita.
- Não há alteração de código, APIs, dados, tabelas ou dependências nesta etapa de planejamento.
- O PDF “Projeto - Gestão de Clínica de Saúde.pdf” não foi encontrado no workspace; a análise parte das decisões deste pedido e dos arquivos disponíveis.
