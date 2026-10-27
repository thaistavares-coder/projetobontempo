## MODIFIED Requirements

### Requirement: Disponibilizar a navegação principal

A aplicação web SHALL disponibilizar a página Início e navegação para os cinco módulos funcionais aprovados: Pacientes, Profissionais (médicos), Especialidades médicas, Consultas e Prontuários.

#### Scenario: Abrir a aplicação

- **WHEN** uma pessoa acessa a aplicação web após a implementação futura do escopo revisado
- **THEN** a página Início é apresentada e a navegação para os cinco módulos aprovados está disponível

#### Scenario: Navegar entre as páginas

- **WHEN** uma pessoa seleciona um módulo funcional na navegação
- **THEN** a aplicação apresenta o módulo selecionado e mantém a página Início e os demais módulos acessíveis

### Requirement: Distinguir a entrega inicial da integração GET posterior

A entrega inicial SHALL permanecer acessível sem realizar chamadas HTTP ao Xano. Uma Change posterior pode integrar somente listagens GET explicitamente aprovadas, mantendo as chamadas reais desabilitadas por padrão e sem alterar retroativamente o comportamento da entrega inicial. O escopo-alvo revisado acrescenta a navegação para Especialidades, Consultas e Prontuários em Changes futuras.

O acesso às páginas da entrega inicial SHALL NOT depender da configuração ou da disponibilidade das APIs do Xano. A configuração de URLs, sem habilitação externa explícita, SHALL NOT iniciar requisições.

#### Scenario: Acessar a entrega inicial sem integração com o Xano

- **WHEN** uma pessoa inicia a versão atualmente implementada e navega entre Início, Pacientes e Profissionais sem URL base configurada e sem APIs do Xano disponíveis
- **THEN** as páginas da primeira entrega são apresentadas e a navegação funciona sem realizar requisições HTTP ao Xano

#### Scenario: Manter a integração GET posterior desabilitada por padrão

- **WHEN** URLs de listagem estão configuradas, mas a integração posterior não foi explicitamente habilitada
- **THEN** as páginas permanecem acessíveis sem chamadas HTTP ao Xano e informam que a integração está desabilitada

### Requirement: Apresentar páginas informativas dos módulos

As páginas Pacientes, Profissionais, Especialidades, Consultas e Prontuários SHALL identificar o respectivo módulo. A apresentação de cada módulo SHALL refletir apenas funcionalidades efetivamente implementadas e não poderá simular consultas, cadastros ou dados clínicos.

#### Scenario: Abrir Pacientes

- **WHEN** uma pessoa seleciona Pacientes na navegação
- **THEN** vê o título do módulo Pacientes e a indicação de que suas funcionalidades dependem de implementação própria

#### Scenario: Abrir Profissionais

- **WHEN** uma pessoa seleciona Profissionais na navegação
- **THEN** vê o título do módulo Profissionais, restrito ao escopo de médicos, e a indicação de que suas funcionalidades dependem de implementação própria

#### Scenario: Abrir Especialidades, Consultas ou Prontuários

- **WHEN** uma pessoa seleciona Especialidades, Consultas ou Prontuários na navegação após suas páginas serem adicionadas em Changes futuras
- **THEN** vê o título do módulo correspondente e a interface não apresenta funcionalidade inexistente como concluída

#### Scenario: Não simular funcionalidade clínica

- **WHEN** um módulo ainda não possui implementação ou fonte real de dados
- **THEN** a página informa seu estado sem simular registros, consultas ou operações

### Requirement: Preservar o escopo funcional da interface

A interface SHALL oferecer Início como página de apresentação e navegação para Pacientes, Profissionais (médicos), Especialidades médicas, Consultas e Prontuários. O sistema SHALL NOT exigir login nem oferecer gerenciamento de usuários ou papéis nesta versão.

Esta Change SHALL limitar-se à revisão de escopo e modelo: não SHALL implementar integração HTTP com Xano, operações clínicas, CRUD, autenticação ou acesso a dados de prontuário. A interface SHALL NOT apresentar dados fictícios de pacientes ou profissionais. A integração GET posterior é delimitada por Change própria, exige habilitação externa explícita e permanece sujeita à confirmação de segurança; chamadas usam APIs HTTP confirmadas, sem acesso direto do frontend ao banco de dados.

#### Scenario: Acessar as páginas sem autenticação ou integração

- **WHEN** uma pessoa navega pela primeira entrega sem login, URL base configurada ou APIs do Xano disponíveis
- **THEN** Início, Pacientes e Profissionais permanecem acessíveis sem chamadas HTTP ao Xano

#### Scenario: Conferir o escopo das páginas

- **WHEN** a Change de revisão de escopo é aplicada
- **THEN** ela altera somente especificações e não habilita login, CRUD, consultas clínicas, agendamentos, disponibilidades, dados fictícios ou acesso a prontuários

#### Scenario: Manter os limites arquiteturais

- **WHEN** uma implementação futura integra o frontend ao backend
- **THEN** o frontend usa somente APIs HTTP confirmadas e não acessa diretamente o banco de dados

## ADDED Requirements

### Requirement: Apresentar cards de navegação para o escopo aprovado

A página Início SHALL apresentar a função institucional e permitir alcançar os cinco módulos funcionais aprovados por navegação. A apresentação não SHALL criar módulo funcional de Agenda separado nem exibir números ou dados clínicos fictícios.

#### Scenario: Acessar um módulo pela página Início

- **WHEN** a pessoa seleciona um card ou link de módulo na página Início
- **THEN** a aplicação navega para o módulo existente correspondente, sem simular dados ou operações

#### Scenario: Apresentar somente o escopo aprovado

- **WHEN** a página Início lista os módulos funcionais
- **THEN** apresenta Pacientes, Profissionais, Especialidades, Consultas e Prontuários, mantendo Início como apresentação e sem adicionar Agenda como módulo autônomo
