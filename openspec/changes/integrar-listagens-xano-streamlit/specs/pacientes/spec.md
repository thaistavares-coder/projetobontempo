## MODIFIED Requirements

### Requirement: Listar pacientes na integração inicial

O sistema SHALL permitir listar pacientes cadastrados. A consulta individual e as operações de escrita são especificadas pela Change `crud-pacientes-profissionais-xano-streamlit`; esta Change define somente o contrato da listagem inicial.

As respostas SHALL incluir somente os dados necessários ao consumidor da API:

- identificador;
- nome;
- telefone;
- e-mail.

Campos internos ou não destinados ao consumidor da API SHALL ser omitidos das respostas. O frontend SHALL exibir os campos básicos da listagem. Esta definição não restringe a consulta individual nem as operações CRUD da Change posterior.

#### Scenario: Listar pacientes cadastrados

- **WHEN** uma solicitação GET válida pede a lista de pacientes
- **THEN** o sistema retorna os pacientes cadastrados com os campos básicos permitidos, incluindo uma lista vazia quando não houver registros

#### Scenario: Integrar a listagem inicial no frontend

- **WHEN** esta Change carrega pacientes para a página Streamlit
- **THEN** usa o endpoint GET de coleção confirmado e mapeia `id`, `nome`, `telefone` e `email`; as demais operações são regidas pela Change CRUD posterior
