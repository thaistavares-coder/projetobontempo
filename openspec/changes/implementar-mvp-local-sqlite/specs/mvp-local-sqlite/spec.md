## Purpose

Define o comportamento e os limites do MVP local de gestão de consultório usado para demonstração, com interface Streamlit e persistência SQLite exclusivamente local.

## ADDED Requirements

### Requirement: Disponibilizar navegação para os módulos locais

A aplicação SHALL disponibilizar as páginas Início, Pacientes, Profissionais, Especialidades e Consultas em modo de demonstração local. A página inicial SHALL oferecer acesso aos módulos e informar que nenhuma alteração é enviada ao Xano.

#### Scenario: Abrir a aplicação de demonstração

- **WHEN** a aplicação é iniciada conforme as instruções locais do frontend
- **THEN** a pessoa usuária pode navegar entre Início, Pacientes, Profissionais, Especialidades e Consultas
- **AND** a interface identifica o uso de SQLite local e informa que não envia alterações ao Xano

### Requirement: Cadastrar e consultar pacientes e profissionais

O sistema SHALL permitir cadastrar e listar pacientes e profissionais no banco SQLite local. Nome e telefone SHALL ser obrigatórios, e-mail SHALL ser opcional e, quando informado, SHALL ter formato validado. O cadastro de profissional SHALL permitir selecionar zero ou mais especialidades existentes.

#### Scenario: Cadastrar registros com dados válidos

- **WHEN** a pessoa usuária informa nome e telefone e, opcionalmente, um e-mail válido
- **THEN** o registro é persistido localmente e aparece na respectiva listagem

#### Scenario: Rejeitar dados obrigatórios ausentes ou e-mail inválido

- **WHEN** a pessoa usuária tenta cadastrar paciente ou profissional sem nome ou telefone, ou informa um e-mail inválido
- **THEN** o sistema apresenta uma mensagem de validação e não salva o registro inválido

#### Scenario: Listagens ainda sem registros

- **WHEN** não há pacientes ou profissionais cadastrados
- **THEN** a página correspondente informa que não existem registros no banco SQLite local

### Requirement: Manter especialidades e vínculos N:N

O sistema SHALL permitir cadastrar especialidades com nome não vazio, listar o catálogo e associar cada profissional a zero ou mais especialidades. O mesmo vínculo entre profissional e especialidade SHALL existir no máximo uma vez, e consultas SHALL usar uma especialidade vinculada ao profissional escolhido.

#### Scenario: Cadastrar e associar especialidades

- **WHEN** a pessoa usuária cadastra especialidades e salva os vínculos de um profissional
- **THEN** os vínculos escolhidos ficam persistidos e podem ser consultados nas páginas de profissionais e consultas

#### Scenario: Impedir especialidade duplicada

- **WHEN** a pessoa usuária tenta cadastrar nome de especialidade que já existe sem distinção de caixa ou espaços externos
- **THEN** o sistema informa que a especialidade já existe e preserva o catálogo

#### Scenario: Não selecionar especialidade de outro profissional na consulta

- **WHEN** a pessoa usuária seleciona um profissional para agendar uma consulta
- **THEN** somente especialidades vinculadas a esse profissional ficam disponíveis para o agendamento

### Requirement: Agendar consultas e controlar seus status

O sistema SHALL permitir agendar uma consulta relacionando paciente, profissional e especialidade, com data e horários inicial e final, e listar os dados relacionados e o status. O horário final SHALL ser posterior ao inicial. Uma nova consulta SHALL iniciar como Agendada. A interface SHALL permitir alterar o status entre Agendada, Confirmada, Realizada, Cancelada e Não compareceu.

#### Scenario: Agendar consulta válida

- **WHEN** a pessoa usuária seleciona paciente, profissional e especialidade vinculada e informa intervalo válido
- **THEN** a consulta fica persistida no SQLite e aparece na listagem com status Agendada

#### Scenario: Rejeitar intervalo inválido ou combinação sem vínculo

- **WHEN** o horário final não é posterior ao inicial ou a especialidade não está vinculada ao profissional
- **THEN** o sistema apresenta erro e não cria a consulta

#### Scenario: Atualizar o status da consulta

- **WHEN** a pessoa usuária escolhe uma consulta e um status disponível
- **THEN** o status escolhido é persistido e mostrado na listagem

### Requirement: Prevenir conflitos de horário do profissional

O sistema SHALL rejeitar intervalos sobrepostos para o mesmo profissional quando ambos ocuparem horário. Consultas Agendadas e Confirmadas SHALL ocupar horário; consultas Realizadas, Canceladas e Não compareceu SHALL liberar o horário. Intervalos adjacentes SHALL ser permitidos. Ao alterar um status para um estado que ocupa horário, o sistema SHALL verificar novamente conflitos.

#### Scenario: Rejeitar consulta sobreposta

- **WHEN** uma pessoa usuária tenta agendar consulta cujo intervalo se sobrepõe a outra consulta Agendada ou Confirmada do profissional
- **THEN** o sistema rejeita a operação e informa o conflito

#### Scenario: Permitir intervalos adjacentes e reutilizar horário liberado

- **WHEN** uma consulta começa exatamente ao fim de outra ou o horário está ocupado apenas por consulta em status que não ocupa horário
- **THEN** o sistema permite o novo agendamento

#### Scenario: Impedir confirmação que criaria conflito

- **WHEN** a pessoa usuária altera uma consulta para Agendada ou Confirmada e existe outra consulta ocupando horário sobreposto para o profissional
- **THEN** o sistema rejeita a alteração e preserva o status anterior

### Requirement: Carregar somente exemplos fictícios mediante ação explícita

O sistema SHALL oferecer uma ação explícita para carregar registros sintéticos de demonstração. A carga SHALL ser recusada quando já houver dados funcionais no banco, sem substituir ou alterar registros existentes.

#### Scenario: Carregar exemplos em banco vazio

- **WHEN** a pessoa usuária solicita carregar exemplos e não há pacientes, profissionais, especialidades, vínculos ou consultas
- **THEN** o sistema insere os registros fictícios de demonstração e informa a conclusão

#### Scenario: Recusar carga em banco com dados

- **WHEN** a pessoa usuária solicita carregar exemplos e já existem dados funcionais
- **THEN** o sistema recusa a carga, informa o motivo e mantém os registros existentes

### Requirement: Restringir o escopo ao modo local de demonstração

Este MVP SHALL usar somente o banco SQLite local para as páginas descritas nesta capability e SHALL armazenar os dados no ambiente local. O modo SHALL ser tratado como demonstração sem autenticação e não SHALL ser apresentado como ambiente seguro para dados reais. Não SHALL disponibilizar prontuários nem cadastro de disponibilidade profissional, nem SHALL realizar integração ativa com Xano.

#### Scenario: Executar sem integração ativa com Xano

- **WHEN** a pessoa usuária utiliza qualquer módulo do MVP local
- **THEN** as operações leem e gravam apenas no SQLite local e não fazem chamadas às APIs do Xano

#### Scenario: Recursos fora do escopo

- **WHEN** a pessoa usuária procura autenticação, prontuários ou disponibilidade profissional
- **THEN** esses recursos não são oferecidos pelo MVP local

### Requirement: Manter legibilidade visual dos formulários

A interface SHALL apresentar rótulos, valores e placeholders dos campos de formulário com contraste legível sobre seus fundos. Os controles em foco e os botões de ação primária SHALL possuir estados visuais distinguíveis.

#### Scenario: Utilizar controles de formulário

- **WHEN** a pessoa usuária visualiza ou interage com formulários do MVP
- **THEN** rótulos, valores, placeholders e estados de foco permanecem visualmente distinguíveis do fundo
