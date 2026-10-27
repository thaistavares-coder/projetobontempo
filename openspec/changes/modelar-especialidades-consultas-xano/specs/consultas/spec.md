## Purpose

Define a estrutura e as regras de integridade de consultas agendadas com paciente, médico, especialidade, data, horário e status, sem incluir autenticação ou conteúdo clínico.

## ADDED Requirements

### Requirement: Vincular cada consulta às entidades obrigatórias

O modelo SHALL exigir que cada consulta referencie exatamente um paciente, um profissional médico, uma especialidade e um status existentes, além dos timestamps obrigatórios `inicio_em` e `fim_em`. O instante final SHALL ser posterior ao inicial e ambos deverão corresponder ao mesmo dia local da clínica, usando `America/Sao_Paulo` como referência proposta, sujeita a confirmação antes da implementação. Uma consulta SHALL NOT exigir prontuário ou registro clínico para existir como agendada.

#### Scenario: Criar consulta com referências válidas

- **WHEN** uma consulta é criada com paciente, médico, especialidade, status e timestamps válidos
- **THEN** cada referência aponta para o respectivo registro existente e a consulta pode ser persistida

#### Scenario: Rejeitar referência inexistente

- **WHEN** paciente, médico, especialidade ou status não existe
- **THEN** a consulta é rejeitada sem referências órfãs nem persistência parcial

#### Scenario: Manter consulta agendada sem dados clínicos

- **WHEN** uma consulta é criada como agendada
- **THEN** não é exigido prontuário nem registro de atendimento para persistir a consulta

### Requirement: Validar compatibilidade entre médico e especialidade

O backend SHALL validar que a especialidade informada na consulta está associada ao médico selecionado no momento da gravação. A mera existência individual do médico e da especialidade SHALL NOT ser suficiente para aceitar a combinação.

#### Scenario: Usar especialidade vinculada ao médico

- **WHEN** a consulta informa uma especialidade associada ao médico
- **THEN** a relação é aceita se as demais referências e regras forem válidas

#### Scenario: Rejeitar especialidade não vinculada ao médico

- **WHEN** a consulta informa especialidade existente que não está associada ao médico selecionado
- **THEN** o backend rejeita a consulta sem persistência parcial

### Requirement: Manter entidade de status de consulta

O modelo SHALL manter `status_consulta` como entidade referenciável pela consulta, não como texto livre não controlado. O catálogo inicial SHALL conter `agendada`, `confirmada`, `realizada`, `cancelada` e `nao_compareceu`; a consulta armazenará somente o status atual, sem tabela de histórico nesta modelagem. As regras de transição SHALL ser definidas antes de implementar APIs de alteração de status.

#### Scenario: Referenciar status existente

- **WHEN** uma consulta recebe um status aprovado e existente no catálogo
- **THEN** a consulta referencia esse registro de status

#### Scenario: Rejeitar status fora do catálogo

- **WHEN** uma consulta recebe um status que não existe ou não está permitido
- **THEN** a operação é rejeitada sem persistência parcial

#### Scenario: Marcar status que ocupa horário

- **WHEN** a consulta recebe status `agendada` ou `confirmada`
- **THEN** esse status ocupa o intervalo para validação de conflitos; `realizada`, `cancelada` e `nao_compareceu` liberam o horário

### Requirement: Prevenir conflitos de horário no backend

O backend SHALL impedir sobreposição entre intervalos `[inicio_em, fim_em)` do mesmo dia local e do mesmo médico quando ambos os status ocupam horário (`agendada` ou `confirmada`). A interpretação do dia local usa `America/Sao_Paulo` como referência proposta, sujeita a confirmação antes da implementação. Intervalos adjacentes cujo fim coincide com o próximo início SHALL ser permitidos. A validação SHALL ocorrer no backend e ser protegida contra criação concorrente de consultas conflitantes; a interface não será o único controle.

#### Scenario: Tentar reservar horário conflitante

- **WHEN** uma nova consulta conflita temporalmente com outra consulta do mesmo médico cujo status ocupa horário
- **THEN** o backend rejeita a nova consulta sem alterar os registros existentes

#### Scenario: Reutilizar horário liberado

- **WHEN** uma consulta anterior deixa de ocupar o horário conforme a política aprovada
- **THEN** uma nova consulta pode usar esse horário se não houver outro conflito

#### Scenario: Criar consultas para médicos distintos

- **WHEN** duas consultas possuem horários coincidentes, mas médicos diferentes
- **THEN** não são consideradas conflitantes por essa regra

#### Scenario: Criar consultas adjacentes

- **WHEN** uma consulta termina exatamente no horário em que a seguinte começa para o mesmo médico
- **THEN** os intervalos não são considerados sobrepostos e ambas podem existir

### Requirement: Preservar registros existentes durante a evolução do esquema

A inclusão de consultas SHALL NOT apagar, substituir ou reidentificar registros existentes de pacientes ou profissionais. A política de exclusão e retenção de registros referenciados SHALL ser definida antes de habilitar operações de remoção, sem cascata destrutiva implícita.

#### Scenario: Preservar referências ao excluir registros relacionados

- **WHEN** um paciente ou médico possui consulta relacionada
- **THEN** a remoção não deixa chave estrangeira órfã nem apaga consultas ou histórico por cascata não aprovada
