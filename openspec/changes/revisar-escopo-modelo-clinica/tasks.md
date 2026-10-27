## 1. Confirmar decisões e evidências do ambiente

- [ ] 1.1 Comparar os arquivos Xano versionados com o ambiente Xano autorizado de destino e registrar tabelas, endpoints, autenticação e publicação confirmados; verificar que diferenças entre local e publicado ficam explicitamente identificadas e que nenhum dado real de paciente é usado.
- [ ] 1.2 Registrar a decisão aprovada de relação N:N Médico–Especialidade, com zero vínculos possíveis durante a transição e vínculo obrigatório para agendamento; obter aprovação das cardinalidades ainda pendentes de Paciente–Prontuário, Prontuário–Registro de Atendimento, Consulta–Registro e Status–Consulta, documentando mínimos, máximos, FKs, unicidade e regras de exclusão.
- [ ] 1.3 Definir e registrar valores, obrigatoriedade, transições e eventual histórico de `STATUS_CONSULTA`; verificar que a entidade permanece no modelo e que regras não decididas estão marcadas como bloqueios de implementação.
- [ ] 1.4 Realizar avaliação de privacidade e acesso para dados clínicos sem login; verificar que controles aprovados de exposição, confidencialidade, auditoria e retenção antecedem qualquer persistência ou disponibilização de prontuários.

## 2. Atualizar a documentação aprovada

- [ ] 2.1 Atualizar `docs/domain-model.md` com as entidades, relações e decisões aprovadas; verificar que cardinalidades não aprovadas permanecem identificadas como pendentes e que a distinção entre Consulta e Registro de Atendimento é explícita.
- [ ] 2.2 Atualizar `docs/project-overview.md` com os cinco módulos, a página Início, a ausência de login/gestão de usuários nesta versão e o estado não implementado das capacidades clínicas; verificar que escopo-alvo não é apresentado como funcionalidade já disponível.
- [ ] 2.3 Revisar as especificações de Pacientes, Profissionais e Interface Web à luz das decisões e manter requisitos de segurança, integração exclusivamente por APIs HTTP e ausência de acesso direto ao banco; verificar que não há contradições com as cardinalidades aprovadas.

## 3. Dividir a implementação futura

- [ ] 3.1 Propor uma Change OpenSpec para esquema Xano e migração de dados com FKs, unicidade, integridade referencial e rollback; verificar que preserva IDs e dados atuais e não remove entidades existentes.
- [ ] 3.2 Propor uma Change OpenSpec para regras de negócio e APIs de Especialidades, Consultas, Status, Prontuários e Registros; verificar que bloqueia exposição clínica até os controles de segurança estarem aprovados.
- [ ] 3.3 Propor uma Change OpenSpec para as páginas Streamlit dos cinco módulos e uma Change separada de integração HTTP, dependente de endpoints e configuração confirmados; verificar que nenhuma proposta inclui acesso do frontend ao banco ou login/gestão de usuários nesta versão.

## 4. Validar o encerramento da revisão

- [ ] 4.1 Validar estritamente as Changes OpenSpec resultantes e revisar `git diff`/`git status`; verificar que esta Change não altera código Python, XanoScript, tabelas, registros ou endpoints e que nenhum teste contém dados reais de pacientes.
