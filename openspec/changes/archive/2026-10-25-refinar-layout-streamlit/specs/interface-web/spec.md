## Purpose

Define a apresentação administrativa refinada das três páginas Streamlit existentes, mantendo claro que as telas de módulos ainda não possuem integração nem operações de negócio.

## ADDED Requirements

### Requirement: Apresentar identidade visual Bontempo consistente

A aplicação SHALL apresentar as páginas Início, Pacientes e Profissionais com cabeçalhos, ícones, hierarquia tipográfica e espaçamentos consistentes, adequados à visualização em notebook e navegador, sem alterar a navegação existente.

#### Scenario: Navegar pelas páginas existentes

- **WHEN** a pessoa abre Início, Pacientes ou Profissionais
- **THEN** cada página mantém a identidade visual comum e a navegação continua oferecendo somente essas três páginas

### Requirement: Navegar pelos cards da página Início

A página Início SHALL apresentar a identidade visual Bontempo, uma breve apresentação do sistema e cards que permitam navegar para Pacientes e Profissionais.

Os cards SHALL indicar Agenda como módulo futuro de forma discreta, sem criar uma página ou oferecer navegação para esse módulo. A página SHALL NOT apresentar indicadores numéricos fictícios.

#### Scenario: Usar os cards de navegação

- **WHEN** a pessoa seleciona o card de Pacientes ou Profissionais na página Início
- **THEN** a aplicação abre a página existente correspondente

#### Scenario: Visualizar o módulo futuro

- **WHEN** a pessoa abre a página Início
- **THEN** Agenda é apresentada apenas como indicação de módulo futuro, sem página própria, ação disponível ou números fictícios

### Requirement: Apresentar estrutura vazia do módulo Pacientes

A página Pacientes SHALL exibir cabeçalho com título e descrição, um campo de busca desabilitado, um botão “Novo paciente” desabilitado, uma tabela vazia com as colunas ID, Nome, Telefone e E-mail e a mensagem “Integração com Xano ainda não disponível”.

A página SHALL NOT apresentar registros de pacientes nem realizar chamadas HTTP ou simular operações.

#### Scenario: Abrir Pacientes sem integração

- **WHEN** a pessoa abre Pacientes sem integração com o Xano
- **THEN** vê o cabeçalho, os controles desabilitados, a tabela sem linhas com as colunas especificadas e a mensagem de integração indisponível, sem chamadas HTTP

#### Scenario: Tentar usar controles do módulo Pacientes

- **WHEN** a pessoa visualiza o campo de busca e o botão “Novo paciente”
- **THEN** ambos estão desabilitados e não iniciam busca, cadastro ou qualquer operação persistida

### Requirement: Apresentar estrutura vazia do módulo Profissionais

A página Profissionais SHALL exibir cabeçalho com título e descrição, um campo de busca desabilitado, um botão “Novo profissional” desabilitado, uma tabela vazia com as colunas ID, Nome e Especialidade e uma mensagem explícita de que a integração futura com Xano ainda não está disponível.

A página SHALL NOT apresentar registros de profissionais nem realizar chamadas HTTP ou simular operações.

#### Scenario: Abrir Profissionais sem integração

- **WHEN** a pessoa abre Profissionais sem integração com o Xano
- **THEN** vê o cabeçalho, os controles desabilitados, a tabela sem linhas com as colunas especificadas e a indicação de integração futura, sem chamadas HTTP

#### Scenario: Tentar usar controles do módulo Profissionais

- **WHEN** a pessoa visualiza o campo de busca e o botão “Novo profissional”
- **THEN** ambos estão desabilitados e não iniciam busca, cadastro ou qualquer operação persistida

### Requirement: Preservar limites funcionais e arquiteturais

A interface SHALL NOT implementar login ou autenticação, chamadas HTTP ao Xano, dados fictícios, CRUD, agendamentos, disponibilidades, novas páginas ou dependências adicionais. Nenhum backend, tabela ou arquivo XanoScript SHALL ser alterado por esta mudança.

#### Scenario: Verificar ausência de integrações e operações

- **WHEN** a pessoa navega pelas três páginas
- **THEN** a aplicação funciona sem autenticação e sem chamadas HTTP, não exibe registros inventados nem oferece operações habilitadas de busca ou gravação
