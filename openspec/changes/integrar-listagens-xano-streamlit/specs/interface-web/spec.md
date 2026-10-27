## MODIFIED Requirements

### Requirement: Preservar navegação e estados da integração

Esta Change especifica a fase inicial de listagem GET; a Change `crud-pacientes-profissionais-xano-streamlit` especifica a evolução para CRUD de Pacientes e Profissionais. A navegação SHALL permanecer disponível independentemente da disponibilidade do Xano. Quando a configuração ou habilitação exigida para uma operação estiver ausente, a interface SHALL apresentar o estado apropriado sem enviar a requisição correspondente. Esta requirement não restringe as operações CRUD especificadas pela Change posterior.

#### Scenario: Acessar as páginas sem integração com o Xano

- **WHEN** uma pessoa inicia a aplicação e navega entre Início, Pacientes e Profissionais sem integração explicitamente habilitada
- **THEN** as três páginas são apresentadas e a navegação funciona sem realizar requisições HTTP ao Xano, com indicação clara de configuração pendente nos módulos de listagem

### Requirement: Apresentar páginas informativas dos módulos

As páginas Pacientes e Profissionais SHALL manter seus títulos, descrições e identidade visual, e exibir nas tabelas os registros retornados pelos respectivos endpoints GET de listagem quando a integração estiver configurada e disponível.

#### Scenario: Abrir Pacientes

- **WHEN** a pessoa seleciona Pacientes na navegação e o GET de listagem retorna registros válidos
- **THEN** vê o título e a descrição do módulo e os registros reais retornados pela API nas colunas previstas

#### Scenario: Abrir Profissionais

- **WHEN** a pessoa seleciona Profissionais na navegação e o GET de listagem retorna registros válidos
- **THEN** vê o título e a descrição do módulo e os registros reais retornados pela API nas colunas previstas, incluindo `especialidade` como texto

#### Scenario: Abrir módulos clínicos ainda não implementados

- **WHEN** uma pessoa consulta a navegação durante esta Change
- **THEN** Especialidades, Consultas e Prontuários não são adicionados ou apresentados como funcionalidades implementadas

### Requirement: Preservar o escopo dos módulos durante a evolução

A fase inicial desta Change limita-se às listagens GET de Pacientes e Profissionais. A Change `crud-pacientes-profissionais-xano-streamlit` define cadastro, edição e exclusão nesses módulos. A aplicação SHALL preservar as demais páginas existentes sem ampliar seu escopo, não exigir login como parte destas Changes e não apresentar dados fictícios como se fossem registros reais. Agendamentos, disponibilidades, prontuários e outras operações clínicas continuam fora do escopo.

#### Scenario: Acessar as páginas sem autenticação ou integração

- **WHEN** uma pessoa inicia a aplicação e navega pelas páginas disponíveis sem login e sem configuração ou disponibilidade do Xano
- **THEN** as três páginas são apresentadas sem exigir autenticação; sem configuração não são feitas requisições e a interface informa a pendência, e com configuração indisponível informa a falha sem inventar dados

#### Scenario: Conferir o escopo das páginas

- **WHEN** a pessoa utiliza a navegação da aplicação
- **THEN** as páginas existentes permanecem disponíveis; Pacientes e Profissionais oferecem somente as operações especificadas pela Change CRUD, sem habilitar agendamentos, disponibilidades ou acesso clínico não especificado

### Requirement: Apresentar a listagem do módulo Pacientes

A fase GET desta Change define a apresentação da listagem de Pacientes com os campos ID, Nome, Telefone e E-mail, exibindo somente registros recebidos do Xano e uma mensagem apropriada para lista vazia. Cadastro, consulta individual, edição e exclusão são definidos pela Change CRUD posterior. A página SHALL NOT simular registros.

#### Scenario: Abrir Pacientes sem integração

- **WHEN** a pessoa abre Pacientes sem integração com o Xano
- **THEN** vê o cabeçalho, os controles desabilitados, a estrutura de tabela com as colunas especificadas e uma indicação de configuração ausente ou de falha, sem registros inventados

#### Scenario: Listar pacientes existentes

- **WHEN** o GET de pacientes retorna uma coleção JSON válida de registros
- **THEN** cada linha da tabela corresponde a um registro retornado e apresenta somente ID, Nome, Telefone e E-mail

#### Scenario: Listar sem pacientes

- **WHEN** o GET de pacientes retorna uma coleção JSON vazia
- **THEN** a tabela não apresenta linhas fictícias e a página informa que não há pacientes cadastrados

### Requirement: Apresentar a listagem do módulo Profissionais

A fase GET desta Change define a apresentação da listagem de Profissionais com os campos ID, Nome e Especialidade, exibindo somente registros recebidos do Xano e uma mensagem apropriada para lista vazia. `especialidade` SHALL permanecer textual, sem exigir catálogo ou relação. Cadastro, consulta individual, edição e exclusão são definidos pela Change CRUD posterior. A página SHALL NOT simular registros.

#### Scenario: Abrir Profissionais sem integração

- **WHEN** a pessoa abre Profissionais sem integração com o Xano
- **THEN** vê o cabeçalho, os controles desabilitados, a estrutura de tabela com as colunas especificadas e uma indicação de configuração ausente ou de falha, sem registros inventados

#### Scenario: Listar profissionais existentes

- **WHEN** o GET de profissionais retorna uma coleção JSON válida de registros
- **THEN** cada linha da tabela corresponde a um registro retornado e apresenta somente ID, Nome e Especialidade textual

#### Scenario: Listar sem profissionais

- **WHEN** o GET de profissionais retorna uma coleção JSON vazia
- **THEN** a tabela não apresenta linhas fictícias e a página informa que não há profissionais cadastrados

### Requirement: Preservar limites de segurança e arquitetura

A interface SHALL NOT implementar login, gerenciamento de usuários, agendamentos, disponibilidades ou acesso direto ao banco. Nenhuma tabela, endpoint ou configuração de segurança do Xano SHALL ser alterada por estas Changes. As operações de Pacientes e Profissionais SHALL usar APIs HTTP confirmadas; nenhuma credencial ou segredo SHALL ser armazenado no código versionado. A segurança dos dados e do acesso remoto continua sujeita à tarefa pendente 1.2 desta Change.

#### Scenario: Verificar ausência de integrações e operações

- **WHEN** a pessoa navega pelas três páginas
- **THEN** a aplicação não exige autenticação, não exibe registros inventados e usa somente as operações Xano especificadas para Pacientes e Profissionais, sem alterar permissões ou credenciais remotas

## ADDED Requirements

### Requirement: Configurar os endpoints de listagem externamente

O frontend SHALL obter, por configuração externa, as URLs completas das listagens GET de pacientes e profissionais. As URLs SHALL NOT ser fixadas no código versionado, e credenciais ou tokens não SHALL ser adicionados para esta integração.

#### Scenario: Executar com URLs configuradas e integração habilitada

- **WHEN** as URLs das listagens estão configuradas e a integração foi explicitamente habilitada após as verificações de segurança
- **THEN** cada página consulta somente a URL GET correspondente ao seu módulo

#### Scenario: Executar sem URL configurada

- **WHEN** a página precisa listar registros mas sua URL não está configurada
- **THEN** a interface informa claramente qual configuração está ausente, não envia requisição e não apresenta uma resposta de sucesso simulada

#### Scenario: Iniciar com integração desabilitada

- **WHEN** as URLs estão configuradas, mas `XANO_LISTAGENS_ENABLED` está ausente ou não está definido como `true`
- **THEN** as páginas informam que a integração está desabilitada e não enviam requisições HTTP

### Requirement: Tratar falhas e respostas inesperadas das listagens

O frontend SHALL tratar erro HTTP, timeout, falha de conexão, JSON inválido e JSON com estrutura incompatível com uma coleção de registros. Em qualquer falha, SHALL informar que os dados não puderam ser carregados e SHALL NOT substituir o resultado por uma coleção vazia ou por registros fictícios.

#### Scenario: O endpoint responde com erro HTTP

- **WHEN** um GET de listagem recebe status HTTP de erro
- **THEN** a página apresenta uma mensagem de falha de carregamento sem declarar lista vazia ou sucesso

#### Scenario: O endpoint excede o timeout ou não pode ser alcançado

- **WHEN** o GET excede o timeout definido ou falha por conexão
- **THEN** a página apresenta uma mensagem de indisponibilidade sem bloquear indefinidamente a interface

#### Scenario: O endpoint retorna JSON inválido ou inesperado

- **WHEN** a resposta não pode ser interpretada como uma coleção JSON com os campos previstos para o módulo
- **THEN** a página apresenta uma mensagem de resposta inesperada e não renderiza dados inventados nem trata a falha como lista vazia

### Requirement: Evitar requisições redundantes e permitir atualização

As respostas das listagens SHALL ser reutilizadas durante reruns da interface por um período de cache limitado a 60 segundos. A pessoa SHALL poder solicitar atualização explícita, invalidando o cache correspondente e buscando novamente a listagem.

#### Scenario: Reexecutar a página dentro do período de cache

- **WHEN** a página é reexecutada por uma interação da interface antes de expirarem 60 segundos e não foi solicitada atualização explícita
- **THEN** a resposta em cache é reutilizada sem um novo GET

#### Scenario: Atualizar listagem explicitamente

- **WHEN** a pessoa solicita atualização da lista de um módulo
- **THEN** o cache daquele módulo é invalidado e a página realiza um novo GET para sua listagem

### Requirement: Proteger a demonstração antes de exibir registros

Antes de habilitar a integração em um ambiente de demonstração, SHALL ser confirmado que os registros acessíveis são exclusivamente fictícios, que o ambiente e os endpoints possuem acesso adequadamente restrito e que existe autorização explícita do grupo. A ausência de credenciais em um GET bem-sucedido SHALL NOT ser considerada comprovação de segurança. O frontend SHALL manter as chamadas desabilitadas por padrão até que essa pré-condição seja atendida.

#### Scenario: Habilitar a integração em demonstração

- **WHEN** a integração é preparada para uso no ambiente de demonstração
- **THEN** a confirmação de dados fictícios e restrição adequada de acesso é registrada antes da exposição dos registros

#### Scenario: Segurança do endpoint não foi confirmada

- **WHEN** a segurança do ambiente ou a natureza fictícia dos registros não foi confirmada
- **THEN** `XANO_LISTAGENS_ENABLED` permanece ausente ou falso e nenhuma chamada real é realizada
