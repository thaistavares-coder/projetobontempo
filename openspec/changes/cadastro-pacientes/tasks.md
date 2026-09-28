# Tasks

## 1. Persistência e validações

- [x] 1.1 Criar a estrutura persistente de pacientes com identificador próprio, nome obrigatório, telefone opcional e e-mail opcional; verificar no Xano que os campos e a geração do identificador correspondem à spec.

- [x] 1.2 Definir os critérios de validação para telefone e e-mail antes da implementação das validações.

- [ ] 1.3 Implementar no backend as validações de nome, telefone e e-mail; verificar que entradas válidas são aceitas e entradas inválidas são rejeitadas sem gravação parcial.

## 2. Cadastro e consulta pela API

- [ ] 2.1 Implementar o cadastro de pacientes no backend; verificar que a resposta contém identificador, nome, telefone e e-mail.

- [ ] 2.2 Verificar que coincidências em nome, telefone ou e-mail não impedem o cadastro de pacientes distintos.

- [ ] 2.3 Implementar a listagem de pacientes; verificar retorno de lista vazia quando não houver registros e retorno somente dos campos permitidos.

- [ ] 2.4 Implementar a consulta individual de paciente por identificador; verificar comportamento para paciente existente e paciente inexistente.

## 3. Edição e remoção pela API

- [ ] 3.1 Implementar edição parcial de nome, telefone e e-mail; verificar preservação dos campos não enviados.

- [ ] 3.2 Verificar na edição as validações dos campos enviados, a imutabilidade do identificador e o retorno de não encontrado para paciente inexistente.

- [x] 3.3 Implementar remoção física de paciente no escopo desta change.

- [ ] 3.4 Verificar que o paciente removido não aparece mais nas consultas e que a tentativa de remover um identificador inexistente retorna erro de não encontrado.

## 4. Verificação integrada

- [x] 4.1 Validar os artefatos XanoScript utilizando as ferramentas disponíveis.

- [ ] 4.2 Executar verificações das operações de cadastro, consulta, edição e remoção.

- [ ] 4.3 Confirmar que entradas inválidas não geram alterações parciais nos dados.

- [x] 4.4 Confirmar que as respostas da API expõem somente identificador, nome, telefone e e-mail.

- [x] 4.5 Confirmar que a tabela e as APIs existentes de `user` permanecem inalteradas.

- [x] 4.6 Confirmar que nenhuma funcionalidade de profissionais, disponibilidades, agendamentos, autenticação ou autorização foi implementada nesta change.