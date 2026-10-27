## MODIFIED Requirements

### Requirement: Listar profissionais na integração inicial

O sistema SHALL permitir listar profissionais cadastrados. A consulta individual e as operações de escrita são especificadas pela Change `crud-pacientes-profissionais-xano-streamlit`; esta Change define somente o contrato da listagem inicial.

As respostas SHALL incluir somente os campos destinados ao consumidor da API: identificador, nome, telefone, e-mail e especialidade.

Campos internos ou não destinados ao consumidor SHALL ser omitidos. O frontend SHALL preservar `especialidade` como texto retornado pelo endpoint, sem implementar catálogo ou relacionamento. Esta definição não restringe as operações CRUD da Change posterior.

#### Scenario: Listar profissionais cadastrados

- **WHEN** uma solicitação GET válida pede a lista de profissionais
- **THEN** o sistema retorna os profissionais cadastrados com os campos permitidos, incluindo uma lista vazia quando não houver registros

#### Scenario: Integrar a listagem inicial no frontend

- **WHEN** esta Change carrega profissionais para a página Streamlit
- **THEN** usa o endpoint GET de coleção confirmado e mapeia `id`, `nome`, `telefone`, `email` e `especialidade` textual; as demais operações são regidas pela Change CRUD posterior
