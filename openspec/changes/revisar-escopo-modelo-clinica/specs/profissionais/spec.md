## ADDED Requirements

### Requirement: Restringir profissionais cadastrados a médicos

O escopo do sistema SHALL tratar Profissionais exclusivamente como médicos. O catálogo de Especialidades SHALL relacionar-se aos médicos em cardinalidade N:N. Durante a transição, um médico poderá possuir zero ou mais vínculos; para agendar uma consulta, a especialidade escolhida SHALL estar vinculada ao médico. Os vínculos SHALL referenciar registros existentes e impedir duplicidade do mesmo par.

#### Scenario: Definir o escopo de profissionais

- **WHEN** o cadastro e a consulta de profissionais forem implementados conforme o escopo revisado
- **THEN** cada profissional representa um médico e não uma categoria genérica de prestador

#### Scenario: Associar zero ou mais especialidades durante a transição

- **WHEN** um médico é relacionado a uma ou mais especialidades
- **THEN** cada associação é um vínculo N:N com o catálogo, sem depender de texto livre duplicado, e o médico pode permanecer sem vínculos durante a transição

#### Scenario: Exigir vínculo para agendamento

- **WHEN** uma consulta é agendada para um médico e uma especialidade
- **THEN** a especialidade informada deve estar vinculada ao médico selecionado; mera existência isolada dos registros não basta
