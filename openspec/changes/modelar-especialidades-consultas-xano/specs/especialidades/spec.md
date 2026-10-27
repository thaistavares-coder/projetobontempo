## Purpose

Define o catálogo de especialidades médicas e sua associação muitos-para-muitos com profissionais médicos, preservando a integridade dos vínculos sem conversão implícita dos dados textuais existentes.

## ADDED Requirements

### Requirement: Manter catálogo de especialidades médicas

O modelo SHALL representar cada especialidade médica como entidade identificável e reutilizável, distinta do texto livre atualmente armazenado no profissional. O nome SHALL ser único após remover espaços externos e ignorar caixa, preservando acentos. A regra física que garante essa normalização SHALL ser verificada no backend e no Xano antes da implementação.

#### Scenario: Referenciar especialidade do catálogo

- **WHEN** uma associação médico-especialidade é criada
- **THEN** ela referencia uma especialidade existente do catálogo, não um nome livre duplicado

#### Scenario: Rejeitar especialidade inexistente

- **WHEN** uma associação referencia uma especialidade sem registro correspondente
- **THEN** o vínculo é rejeitado e os dados existentes permanecem inalterados

#### Scenario: Rejeitar nomes duplicados após normalização

- **WHEN** um nome de especialidade difere de outro apenas por espaços externos ou caixa
- **THEN** o sistema trata os nomes como duplicados e rejeita o segundo cadastro

### Requirement: Permitir relação muitos-para-muitos entre médicos e especialidades

O modelo SHALL permitir que um médico tenha múltiplas especialidades e que uma especialidade seja associada a múltiplos médicos por meio de vínculos individualizados. Cada vínculo SHALL apontar para exatamente um profissional e uma especialidade existentes.

#### Scenario: Associar várias especialidades a um médico

- **WHEN** um médico possui vínculos com mais de uma especialidade cadastrada
- **THEN** cada vínculo é representado separadamente e todos se referem ao mesmo médico

#### Scenario: Associar vários médicos a uma especialidade

- **WHEN** uma especialidade é vinculada a médicos distintos
- **THEN** cada associação é mantida como vínculo independente para a mesma especialidade

### Requirement: Impedir vínculos duplicados

O modelo SHALL impedir mais de um vínculo ativo para o mesmo par de médico e especialidade, mantendo distintos os vínculos que tenham apenas um dos lados em comum.

#### Scenario: Rejeitar duplicidade do mesmo par

- **WHEN** se tenta associar novamente um médico à mesma especialidade
- **THEN** a duplicidade é rejeitada sem criar um segundo vínculo para o par

#### Scenario: Permitir vínculos distintos

- **WHEN** um médico é associado a outra especialidade ou outra pessoa médica é associada à mesma especialidade
- **THEN** o vínculo distinto é aceito se ambos os registros existirem

### Requirement: Não migrar automaticamente a especialidade textual existente

A introdução do catálogo e dos vínculos SHALL NOT converter, apagar ou sobrescrever automaticamente `profissional.especialidade`. Qualquer reconciliação futura SHALL ser planejada e aprovada separadamente, com mapeamento revisável, preservação de valores não correspondentes e estratégia de rollback.

#### Scenario: Planejar nova associação sem migração implícita

- **WHEN** o modelo relacional é introduzido em uma Change futura
- **THEN** os valores textuais existentes permanecem intactos até que uma migração explícita seja aprovada

#### Scenario: Valor textual sem correspondência

- **WHEN** um valor textual existente não corresponde inequivocamente a uma especialidade do catálogo
- **THEN** ele não é associado por aproximação nem descartado automaticamente
