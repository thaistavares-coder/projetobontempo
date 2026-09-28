# Spec Delta

## Purpose

Define o comportamento observável para cadastrar, consultar, editar e remover pacientes, mantendo somente dados básicos de identificação e contato sob validação do backend.

## ADDED Requirements

### Requirement: Cadastrar paciente

O sistema SHALL permitir cadastrar um paciente com nome e dados básicos de contato.

O nome SHALL ser obrigatório e não poderá estar vazio nem conter somente espaços.

Telefone e e-mail poderão ser informados. Quando presente, o telefone SHALL conter de 8 a 15 dígitos, poderá usar espaços, parênteses e hífens como formatação e poderá ter um único sinal `+` somente no início. O e-mail SHALL ser validado como endereço de e-mail pelo backend; espaços externos serão removidos antes da validação.

O sistema SHALL atribuir ao paciente um identificador próprio, sem utilizar dados pessoais como identificador.

#### Scenario: Cadastro válido

- **WHEN** uma solicitação de cadastro contém um nome válido e dados de contato ausentes ou válidos
- **THEN** o sistema persiste o paciente e retorna seu identificador e os dados básicos cadastrados

#### Scenario: Cadastro com nome ausente ou inválido

- **WHEN** uma solicitação de cadastro não contém nome ou contém nome vazio ou somente espaços
- **THEN** o sistema rejeita a solicitação com erro de validação e não persiste o paciente

#### Scenario: Cadastro com contato em formato inválido

- **WHEN** uma solicitação contém telefone ou e-mail que não atendem aos critérios de validação definidos
- **THEN** o sistema rejeita a solicitação com erro de validação e não persiste o paciente

---

### Requirement: Consultar pacientes

O sistema SHALL permitir listar pacientes cadastrados e consultar um paciente individualmente pelo identificador.

As respostas SHALL incluir somente os dados necessários ao consumidor da API, como identificador, nome, telefone e e-mail.

Campos internos ou não destinados ao consumidor da API SHALL ser omitidos das respostas.

#### Scenario: Listar pacientes cadastrados

- **WHEN** uma solicitação válida pede a lista de pacientes
- **THEN** o sistema retorna os pacientes cadastrados com os campos básicos permitidos, incluindo uma lista vazia quando não houver registros

#### Scenario: Consultar paciente existente

- **WHEN** uma solicitação válida informa o identificador de um paciente existente
- **THEN** o sistema retorna os dados básicos permitidos daquele paciente

#### Scenario: Consultar paciente inexistente

- **WHEN** uma solicitação informa um identificador sem paciente correspondente
- **THEN** o sistema retorna um erro de não encontrado sem expor dados de outros pacientes

---

### Requirement: Editar paciente

O sistema SHALL permitir editar nome, telefone e e-mail de um paciente existente.

Campos não enviados SHALL preservar seus valores atuais.

Quando o nome for enviado, ele não poderá estar vazio nem conter somente espaços.

Quando telefone ou e-mail forem enviados, deverão respeitar os critérios de validação definidos para esses campos: telefone de 8 a 15 dígitos com formatação permitida e e-mail válido após remover espaços externos.

A edição não poderá alterar o identificador do paciente.

#### Scenario: Editar dados válidos

- **WHEN** uma solicitação válida atualiza um ou mais dados de um paciente existente
- **THEN** o sistema persiste as alterações, preserva os campos não enviados e retorna os dados básicos atualizados

#### Scenario: Editar com dados inválidos

- **WHEN** uma solicitação de edição envia nome vazio ou contendo somente espaços, telefone inválido ou e-mail inválido
- **THEN** o sistema rejeita a solicitação sem aplicar alterações

#### Scenario: Editar paciente inexistente

- **WHEN** uma solicitação de edição informa um identificador sem paciente correspondente
- **THEN** o sistema retorna um erro de não encontrado e não cria um novo paciente

---

### Requirement: Remover paciente

O sistema SHALL permitir remover um paciente existente pelo identificador.

A remoção SHALL retirar o cadastro das consultas posteriores.

O sistema não poderá remover outro registro quando o identificador informado não existir.

Nesta change, a remoção de paciente poderá ser implementada sem considerar relacionamentos futuros com agendamentos, pois esses relacionamentos estão fora do escopo atual.

#### Scenario: Remover paciente existente

- **WHEN** uma solicitação válida remove um paciente existente
- **THEN** o sistema confirma a remoção e o paciente deixa de aparecer nas consultas

#### Scenario: Remover paciente inexistente

- **WHEN** uma solicitação de remoção informa um identificador sem paciente correspondente
- **THEN** o sistema retorna um erro de não encontrado

---

### Requirement: Validar operações no backend

O sistema SHALL aplicar no backend as validações de campos e a verificação de existência do paciente para operações por identificador.

Falhas SHALL retornar erros consistentes e não poderão deixar alterações parciais nos dados do paciente.

O backend SHALL validar telefone com os critérios definidos nesta capability e validar e-mail usando o tipo nativo de e-mail do Xano.

#### Scenario: Rejeitar dados inválidos sem persistência parcial

- **WHEN** uma operação de criação ou edição não atende às validações definidas
- **THEN** o sistema informa erro de validação e mantém os dados persistidos sem alterações parciais

#### Scenario: Não deduplicar por dados de contato compartilháveis

- **WHEN** um novo paciente informa nome, telefone ou e-mail que também constam em outro cadastro
- **THEN** o sistema não rejeita o cadastro somente por essa coincidência e mantém identificadores distintos para os pacientes