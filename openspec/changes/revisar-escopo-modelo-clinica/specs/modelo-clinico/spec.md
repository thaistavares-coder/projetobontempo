## Purpose

Registrar o modelo conceitual aprovado para a clínica, distinguindo decisões do grupo de cardinalidades ainda pendentes e de capacidades que não existem na implementação local.

## ADDED Requirements

### Requirement: Respeitar o escopo funcional aprovado sem usuários ou login

O escopo funcional SHALL contemplar Pacientes, Profissionais exclusivamente médicos, Especialidades médicas, Consultas e Prontuários. A página Início SHALL permanecer como apresentação e navegação, não como módulo clínico adicional.

O escopo SHALL NOT incluir login nem gerenciamento de usuários ou papéis nesta versão. A existência de tabela ou endpoints de usuário em artefatos locais não SHALL, por si só, constituir requisito funcional ou autorização para removê-los.

#### Scenario: Conferir o escopo da versão

- **WHEN** o escopo funcional da clínica é revisado
- **THEN** os cinco módulos aprovados e a página Início são identificados, sem incluir login ou gerenciamento de usuários e papéis

#### Scenario: Encontrar recursos locais de usuário

- **WHEN** a revisão encontra tabela ou endpoints locais de usuário
- **THEN** registra-os como recursos existentes a avaliar, sem presumir que sejam requisito aprovado, que estejam publicados ou que devam ser excluídos

### Requirement: Separar consulta e registro clínico

Uma Consulta SHALL relacionar um paciente, um médico e um status, além dos dados necessários à agenda. Diagnóstico, anotações clínicas e conduta SHALL pertencer a REGISTRO_ATENDIMENTO, não ser duplicados como atributos clínicos de CONSULTA.

Uma consulta apenas agendada SHALL NOT exigir REGISTRO_ATENDIMENTO. Uma consulta realizada poderá gerar no máximo um registro clínico próprio associado à consulta e ao prontuário do paciente.

#### Scenario: Manter uma consulta agendada sem registro clínico

- **WHEN** uma consulta está somente agendada
- **THEN** a consulta pode existir sem REGISTRO_ATENDIMENTO

#### Scenario: Registrar atendimento realizado

- **WHEN** uma consulta é realizada e gera um registro clínico
- **THEN** REGISTRO_ATENDIMENTO referencia a consulta e o prontuário do paciente, e contém diagnóstico, anotações clínicas e conduta

#### Scenario: Evitar duplicação de conteúdo clínico na consulta

- **WHEN** o modelo de CONSULTA e REGISTRO_ATENDIMENTO é definido
- **THEN** diagnóstico, anotações clínicas e conduta são atribuídos ao registro clínico, sem duplicação em CONSULTA

### Requirement: Preservar o prontuário longitudinal do paciente

Um paciente poderá possuir zero ou um PRONTUARIO, e todo PRONTUARIO SHALL pertencer a exatamente um paciente. O prontuário SHALL organizar os registros de atendimento que formam o histórico clínico do paciente.

A interpretação de que um prontuário pode conter vários REGISTROS_ATENDIMENTO é uma proposta coerente com o histórico, mas a cardinalidade exata deverá ser confirmada pelo grupo antes da implementação.

#### Scenario: Paciente sem prontuário

- **WHEN** um paciente ainda não possui histórico clínico registrado
- **THEN** o paciente pode existir sem PRONTUARIO

#### Scenario: Manter histórico clínico associado ao paciente

- **WHEN** há registros clínicos de um paciente
- **THEN** cada registro pertence ao prontuário desse paciente, sem permitir prontuários duplicados para o mesmo paciente

#### Scenario: Confirmar cardinalidade do prontuário

- **WHEN** a modelagem física é preparada
- **THEN** a cardinalidade de PRONTUARIO para REGISTRO_ATENDIMENTO está explicitamente aprovada, sem transformar a notação ambígua “PRONTUARIO 1 REGISTRO_ATENDIMENTO” em uma restrição presumida

### Requirement: Manter STATUS_CONSULTA no modelo e definir sua integridade

STATUS_CONSULTA SHALL permanecer como entidade conceitual relacionada a CONSULTA. A regra candidata é que cada consulta possua exatamente um status atual e que um status possa ser referenciado por várias consultas; catálogo permitido, transições, histórico de mudanças e obrigatoriedade deverão ser confirmados antes da implementação.

#### Scenario: Preservar a entidade de status

- **WHEN** o modelo conceitual de consultas é revisado
- **THEN** STATUS_CONSULTA continua representado como entidade, e não é descartado em favor de texto livre sem aprovação

#### Scenario: Revisar status e transições

- **WHEN** as regras de status são especificadas para implementação
- **THEN** valores permitidos, status inicial, transições e eventual histórico estão documentados e aprovados

### Requirement: Confirmar cardinalidades e restrições antes da implementação

Antes de implementar o modelo clínico, a especificação SHALL documentar para cada relação suas cardinalidades mínima e máxima, chaves estrangeiras, unicidade, obrigatoriedade, comportamento de exclusão e consistência transacional.

A relação MÉDICO–ESPECIALIDADE é N:N: um médico pode ter zero ou mais vínculos durante a transição e uma especialidade pode estar vinculada a zero ou mais médicos. Uma consulta só poderá ser agendada com uma especialidade efetivamente vinculada ao médico escolhido. A implementação deverá definir FKs e impedir duplicidade do par médico-especialidade.

#### Scenario: Preservar a cardinalidade aprovada de especialidades

- **WHEN** o modelo físico de médicos e especialidades é proposto
- **THEN** implementa a relação N:N aprovada, permite zero vínculos por médico durante a transição e documenta FKs, unicidade do par e a exigência de vínculo para agendar consultas

#### Scenario: Evitar implementação com integridade indefinida

- **WHEN** ainda há cardinalidade, unicidade, chave estrangeira ou regra de exclusão clínica pendente além da relação N:N Médico–Especialidade aprovada
- **THEN** a implementação dependente dessa regra permanece bloqueada até a decisão ser registrada

### Requirement: Avaliar proteção de dados clínicos sem presumir autenticação

Antes de persistir ou disponibilizar dados de prontuário e atendimento por API ou interface, a mudança que implementar essa capacidade SHALL apresentar e obter aprovação para controles de confidencialidade, acesso, exposição, retenção e auditoria compatíveis com a decisão de não incluir login ou gestão de usuários nesta versão.

A ausência de login SHALL NOT ser interpretada como autorização para acesso público ou irrestrito a dados clínicos. Esta Change não SHALL implementar autenticação nem os controles compensatórios.

#### Scenario: Planejar acesso a dados clínicos

- **WHEN** uma implementação futura pretende persistir ou expor dados clínicos
- **THEN** os controles de proteção e os riscos decorrentes da ausência de login estão documentados e aprovados antes de habilitar o acesso

#### Scenario: Não presumir exposição pública

- **WHEN** o sistema não oferece login nesta versão
- **THEN** a ausência de login não é usada para justificar acesso público ou irrestrito a pacientes, consultas ou prontuários
