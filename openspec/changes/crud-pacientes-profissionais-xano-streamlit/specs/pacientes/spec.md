## ADDED Requirements

### Requirement: Disponibilizar CRUD de pacientes na interface usando o Xano

A interface SHALL permitir criar, listar, consultar, editar e remover pacientes utilizando exclusivamente endpoints HTTP do Xano confirmados para cada operação. As respostas e os campos SHALL respeitar o contrato confirmado, expondo somente os dados básicos de paciente definidos pela capability. A configuração ausente, falha de transporte, resposta HTTP de erro ou resposta incompatível SHALL ser apresentada como falha explícita, sem simular sucesso nem substituir o resultado por uma lista vazia.

#### Scenario: Cadastrar paciente pela interface

- **WHEN** a pessoa usuária envia um cadastro válido e a integração está configurada
- **THEN** a interface envia a operação ao endpoint Xano confirmado e apresenta sucesso somente após resposta bem-sucedida

#### Scenario: Listar e consultar pacientes

- **WHEN** a página de Pacientes solicita a coleção ou um paciente existente
- **THEN** os dados são obtidos do Xano e a interface exibe somente os campos permitidos pelo contrato

#### Scenario: Editar paciente existente

- **WHEN** a pessoa usuária atualiza campos de um paciente existente
- **THEN** a interface envia a alteração ao endpoint Xano confirmado, preserva campos não enviados conforme o contrato e apresenta o resultado real da operação

#### Scenario: Confirmar exclusão de paciente

- **WHEN** a pessoa usuária solicita remover um paciente e confirma explicitamente a ação
- **THEN** a interface envia a exclusão ao endpoint Xano confirmado e apresenta sucesso somente após resposta bem-sucedida

#### Scenario: Cancelar exclusão de paciente

- **WHEN** a pessoa usuária inicia uma exclusão e cancela a confirmação
- **THEN** a interface não envia uma requisição de exclusão

#### Scenario: Tratar configuração ou resposta inválida

- **WHEN** a configuração da API está ausente ou uma operação retorna falha HTTP, de transporte ou formato inesperado
- **THEN** a interface informa a falha sem alegar que a operação foi concluída e sem ocultá-la como lista vazia

#### Scenario: Não usar registros existentes como dados de teste destrutivo

- **WHEN** operações de integração são verificadas em um ambiente remoto
- **THEN** os testes de criação, edição e exclusão utilizam somente registros sintéticos criados para o teste e não alteram nem removem registros preexistentes
