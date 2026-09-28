# Proposal

## Why

O consultório ainda não possui uma capacidade especificada para manter o cadastro das pessoas que receberão atendimento.

Sem esse cadastro, não é possível identificar pacientes de forma consistente nem preparar os relacionamentos necessários para funcionalidades futuras, como agendamentos.

Esta change cria a primeira capacidade de domínio do sistema, mantendo o escopo limitado ao gerenciamento de pacientes e concentrando validações e integridade no backend Xano.

## What Changes

- Criar o cadastro persistido de pacientes com informações básicas de identificação e contato.
- Disponibilizar operações de criação, consulta de lista, consulta individual, edição e remoção de pacientes.
- Validar no backend os campos obrigatórios, formatos básicos e existência do paciente antes de operações por identificador.
- Evitar exposição desnecessária de campos internos ou sensíveis nas respostas da API.
- Definir respostas de erro consistentes para dados inválidos e paciente inexistente.
- Permitir que pacientes distintos possuam dados de contato coincidentes quando isso não for suficiente para caracterizar duplicidade.
- Manter fora do escopo profissionais, disponibilidades, agendamentos, autenticação completa e qualquer relacionamento com essas entidades.

## Capabilities

### New Capabilities

- `pacientes`: cadastro e gerenciamento básico de pacientes, incluindo identificação, contato e operações CRUD.

### Modified Capabilities

Nenhuma.

## Impact

- Backend Xano/XanoScript: nova estrutura persistente para pacientes e operações relacionadas ao cadastro e gerenciamento.
- Contrato da API: novas entradas, respostas e erros relacionados a pacientes.
- Validação: regras de integridade e validação deverão ser executadas no backend.
- Dependências futuras: agendamentos poderão referenciar pacientes posteriormente, mas nenhum relacionamento com agendamentos será implementado nesta change.
- Dados existentes: a estrutura e as APIs de `user` existentes não serão modificadas por esta change.
- Remoção: nesta change, a remoção de pacientes será tratada sem considerar vínculos futuros com agendamentos, pois esses relacionamentos ainda estão fora do escopo.