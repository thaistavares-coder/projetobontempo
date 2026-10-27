## Purpose

Define a consistent and professional visual presentation for the existing Streamlit pages without adding business functionality or requiring backend services.

## ADDED Requirements

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
