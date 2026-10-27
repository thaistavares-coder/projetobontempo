## ADDED Requirements

### Requirement: Compatibilizar especialidade textual e vínculo relacional futuro

O modelo futuro SHALL permitir associar um profissional a múltiplas especialidades por vínculos com o catálogo. O campo textual `profissional.especialidade` deverá permanecer preservado durante a transição; esta Change não autoriza removê-lo, alterá-lo, convertê-lo automaticamente nem alterar o contrato dos endpoints existentes.

#### Scenario: Preservar compatibilidade de endpoints existentes

- **WHEN** as tabelas relacionais futuras são planejadas ou introduzidas
- **THEN** os endpoints atuais continuam preservando o comportamento e o campo textual de especialidade até uma Change de API aprovada

#### Scenario: Migrar especialidade em etapa separada

- **WHEN** o grupo aprova uma futura reconciliação do texto legado com o catálogo
- **THEN** a migração é especificada separadamente, revisável, sem perda de dados e com rollback
