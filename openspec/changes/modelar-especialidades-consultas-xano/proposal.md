## Why

O modelo Xano versionado ainda não representa especialidades relacionais nem consultas, enquanto o domínio prevê médicos com múltiplas especialidades e consultas agendadas com status. Planejar essas estruturas antes de implementá-las permite definir integridade, conflitos e compatibilidade com os dados e endpoints atuais sem sobrescrever ou migrar dados implicitamente.

## What Changes

- Propor a estrutura conceitual e física de `especialidade`, `profissional_especialidade`, `status_consulta` e `consulta`, com atributos, tipos, chaves, cardinalidades, restrições e regras pendentes de aprovação.
- Especificar a associação N:N entre médico e especialidade e impedir vínculos duplicados.
- Especificar consultas ligadas a paciente, médico, especialidade e status, usando `inicio_em` e `fim_em` como timestamps e validando que a especialidade escolhida pertence ao médico.
- Planejar verificação de conflitos de horário no backend e preservar histórico de consultas canceladas sem apagar ou sobrescrever registros atuais.
- Manter o campo textual `profissional.especialidade` durante uma transição explícita; não fazer conversão automática para a tabela associativa.
- Definir as decisões, verificações do Xano publicado, dependências e ordem para Changes futuras de esquema, APIs/regras e interface.

**Fora do escopo:** criar ou alterar tabelas, índices, registros, endpoints, frontend ou configuração publicada do Xano; executar migração; alterar endpoints existentes; remover ou sobrescrever dados; implementar login ou autenticação; expor dados clínicos; incluir prontuários ou registros de atendimento nesta modelagem; realizar commit, push ou archive.

## Capabilities

### New Capabilities

- `especialidades`: catálogo médico e associação N:N entre médicos e especialidades, incluindo unicidade e integridade do vínculo.
- `consultas`: estrutura e integridade de consultas agendadas, status, vínculo com paciente/médico/especialidade e prevenção de conflitos.

### Modified Capabilities

- `profissionais`: compatibilizar a especialidade textual existente com a associação relacional futura, preservando o valor atual até uma migração explicitamente planejada e aprovada.

## Impact

- Evidências locais: `xano/table/` versiona `paciente`, `profissional` e `user`; `profissional.especialidade` é texto opcional. Não foram encontradas definições versionadas para `especialidade`, `profissional_especialidade`, `status_consulta` ou `consulta`. Isso não confirma a estrutura publicada no Xano.
- Diagnóstico somente de leitura: a branch Xano disponível `v1` está marcada como live e não foi identificada branch de desenvolvimento. O `workspace push --dry-run` apontou alterações locais em recursos existentes (`profissional`, função `validar_telefone_paciente`, grupo `Profissionais` e três endpoints existentes) e referências não resolvidas em addons/funções de exemplo; nenhum push foi realizado. Um push amplo está bloqueado até isolar e revisar o escopo em destino não-live autorizado.
- Os endpoints locais de pacientes e profissionais incluem CRUD; o GET de profissionais ainda devolve `especialidade` textual. A Change `integrar-listagens-xano-streamlit` consome apenas esses GETs e requer preservação do contrato, sem implementar catálogo ou associação.
- A Change ativa `revisar-escopo-modelo-clinica` aprova a relação N:N Médico–Especialidade com zero vínculos durante a transição e vínculo obrigatório para agendar; outras cardinalidades, status e regras de exclusão permanecem pendentes. Esta Change não altera aquela revisão e mantém decisões físicas pendentes sujeitas a aprovação.
- Próximas Changes deverão separar esquema/migração reversível, regras e APIs e, posteriormente, integração das interfaces. Nenhuma chamada real, migração ou alteração física é autorizada por este planejamento.
- Dados são destinados a demonstração acadêmica local e exclusivamente fictícios conforme o contexto informado. A ausência de login não comprova controle de acesso: não disponibilizar dados pessoais ou clínicos antes da verificação e aprovação das salvaguardas no ambiente de destino.
