## Purpose

Define o comportamento inicial da interface web do consultório, incluindo sua navegação principal e os limites seguros de comunicação com as APIs HTTP do Xano.

## ADDED Requirements

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
