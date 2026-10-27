# interface-web Specification

## Purpose

Define o comportamento inicial da interface web do consultório, incluindo sua navegação principal e os limites seguros de comunicação com as APIs HTTP do Xano.

## Requirements

### Requirement: Disponibilizar a navegação principal

A aplicação web SHALL disponibilizar páginas acessíveis para Início, Pacientes e Profissionais por meio da navegação do Streamlit.

#### Scenario: Abrir a aplicação

- **WHEN** uma pessoa acessa a aplicação web
- **THEN** a página Início é apresentada e a navegação para Pacientes e Profissionais está disponível

#### Scenario: Navegar entre as páginas

- **WHEN** uma pessoa seleciona Pacientes ou Profissionais na navegação
- **THEN** a aplicação apresenta a página selecionada e mantém as demais opções de navegação disponíveis

### Requirement: Manter a primeira entrega sem integração HTTP

A primeira entrega SHALL limitar-se à estrutura inicial da aplicação Streamlit e à navegação entre Início, Pacientes e Profissionais, sem realizar chamadas HTTP ao Xano.

O acesso às três páginas SHALL NOT depender da configuração ou da disponibilidade das APIs do Xano. Esta restrição aplica-se à primeira entrega e não altera os requisitos de arquitetura e segurança que regem integrações futuras.

#### Scenario: Acessar as páginas sem integração com o Xano

- **WHEN** uma pessoa inicia a aplicação e navega entre Início, Pacientes e Profissionais sem URL base configurada e sem APIs do Xano disponíveis
- **THEN** as três páginas são apresentadas e a navegação funciona sem realizar requisições HTTP ao Xano

### Requirement: Respeitar a integração frontend-backend

O frontend SHALL obter dados do sistema por meio das APIs HTTP existentes do Xano e SHALL NOT acessar diretamente o banco de dados do Xano.

O frontend SHALL utilizar somente endpoints confirmados e correspondentes às capacidades existentes de pacientes e profissionais. Esta Change não SHALL introduzir operações de agendamento ou disponibilidade.

#### Scenario: Consultar dados de uma capacidade existente

- **WHEN** uma página do frontend precisar consultar dados de pacientes ou profissionais
- **THEN** a consulta é realizada por uma API HTTP existente do Xano, sem conexão direta ao banco de dados

#### Scenario: Não há endpoint confirmado para uma operação

- **WHEN** uma operação solicitada não possui endpoint Xano existente e confirmado
- **THEN** o frontend não inventa nem chama uma rota presumida para essa operação

### Requirement: Manter configuração e credenciais fora do código versionado

O frontend SHALL obter a URL base das APIs e quaisquer credenciais necessárias por configuração externa ao código-fonte versionado.

O frontend SHALL NOT conter tokens, senhas ou URLs sensíveis fixados no código ou em arquivos versionados.

#### Scenario: Executar com configuração externa

- **WHEN** a aplicação precisa se conectar às APIs do Xano
- **THEN** os valores de URL e autenticação são lidos de configuração externa, e não de valores sensíveis embutidos no código

#### Scenario: Configuração obrigatória ausente

- **WHEN** a aplicação precisa fazer uma chamada à API e a configuração necessária não está disponível
- **THEN** a aplicação informa claramente que a configuração está pendente ou ausente e não simula uma resposta bem-sucedida

### Requirement: Apresentar identidade visual consistente

A interface SHALL apresentar Início, Pacientes e Profissionais com uma identidade visual profissional e consistente, usando uma paleta predominantemente azul e verde-água, fundo claro e navegação lateral.

#### Scenario: Navegar entre páginas com identidade consistente

- **WHEN** a pessoa abre Início, Pacientes ou Profissionais
- **THEN** cada página mantém a identidade visual comum e a navegação lateral permanece disponível

### Requirement: Apresentar informações institucionais na página Início

A página Início SHALL apresentar uma breve descrição do sistema e cards informativos relacionados aos módulos existentes, sem exibir ou sugerir dados de pacientes ou profissionais que não tenham sido fornecidos por uma fonte real.

#### Scenario: Abrir a página Início

- **WHEN** a pessoa abre Início
- **THEN** vê uma descrição breve do sistema e cards informativos sem registros, contagens ou exemplos fictícios de pacientes ou profissionais

### Requirement: Apresentar páginas informativas dos módulos

As páginas Pacientes e Profissionais SHALL apresentar o título correspondente ao módulo e informar que suas funcionalidades serão implementadas futuramente.

#### Scenario: Abrir Pacientes

- **WHEN** a pessoa seleciona Pacientes na navegação
- **THEN** vê o título do módulo Pacientes e uma indicação de que suas funcionalidades serão implementadas futuramente

#### Scenario: Abrir Profissionais

- **WHEN** a pessoa seleciona Profissionais na navegação
- **THEN** vê o título do módulo Profissionais e uma indicação de que suas funcionalidades serão implementadas futuramente

### Requirement: Preservar o escopo funcional da interface

A interface SHALL manter somente as páginas Início, Pacientes e Profissionais e SHALL NOT exigir login, realizar chamadas HTTP ao Xano, apresentar dados fictícios de pacientes ou profissionais, implementar CRUD, agendamentos ou disponibilidades, nem alterar o backend.

#### Scenario: Acessar as páginas sem autenticação ou integração

- **WHEN** a pessoa inicia a aplicação e navega pelas páginas disponíveis sem login e sem configuração ou disponibilidade do Xano
- **THEN** as três páginas são apresentadas sem chamadas HTTP ao Xano e sem depender de serviços do backend

#### Scenario: Conferir o escopo das páginas

- **WHEN** a pessoa utiliza a navegação da aplicação
- **THEN** somente Início, Pacientes e Profissionais estão disponíveis e nenhuma operação de cadastro, consulta de dados, agendamento ou disponibilidade é oferecida

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
