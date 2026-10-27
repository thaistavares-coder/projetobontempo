## ADDED Requirements

### Requirement: Disponibilizar CRUD de profissionais na interface usando o Xano

A interface SHALL permitir criar, listar, consultar, editar e remover profissionais utilizando exclusivamente endpoints HTTP do Xano confirmados para cada operação. A resposta SHALL preservar a especialidade como texto legado enquanto o catálogo relacional estiver fora desta mudança. Os campos e validações SHALL respeitar o contrato confirmado; erros de configuração, transporte, HTTP ou formato SHALL ser explícitos e não poderão ser apresentados como sucesso.

#### Scenario: Cadastrar profissional pela interface

- **WHEN** a pessoa usuária envia um cadastro válido e a integração está configurada
- **THEN** a interface envia a operação ao endpoint Xano confirmado e apresenta sucesso somente após resposta bem-sucedida

#### Scenario: Listar e consultar profissionais

- **WHEN** a página de Profissionais solicita a coleção ou um profissional existente
- **THEN** os dados são obtidos do Xano e incluem somente os campos permitidos pelo contrato, preservando a especialidade textual existente

#### Scenario: Editar profissional existente

- **WHEN** a pessoa usuária atualiza dados de um profissional existente
- **THEN** a interface envia a alteração ao endpoint Xano confirmado e apresenta o resultado real da operação, preservando campos não enviados conforme o contrato

#### Scenario: Confirmar exclusão de profissional

- **WHEN** a pessoa usuária solicita remover um profissional e confirma explicitamente a ação
- **THEN** a interface envia a exclusão ao endpoint Xano confirmado e apresenta sucesso somente após resposta bem-sucedida

#### Scenario: Cancelar exclusão de profissional

- **WHEN** a pessoa usuária inicia uma exclusão e cancela a confirmação
- **THEN** a interface não envia uma requisição de exclusão

#### Scenario: Tratar configuração ou resposta inválida

- **WHEN** a configuração da API está ausente ou uma operação retorna falha HTTP, de transporte ou formato inesperado
- **THEN** a interface informa a falha sem alegar que a operação foi concluída

#### Scenario: Não usar registros existentes como dados de teste destrutivo

- **WHEN** operações de integração são verificadas em um ambiente remoto
- **THEN** os testes de criação, edição e exclusão utilizam somente registros sintéticos criados para o teste e não alteram nem removem registros preexistentes
