# Design

## Context

Ver [proposal.md - Why](proposal.md#why) para a motivação e [specs/pacientes/spec.md](specs/pacientes/spec.md) para o contrato de comportamento.

O Xano é o backend previsto no projeto. As validações de dados e as regras de integridade deverão ser aplicadas no backend.

Esta change está limitada ao cadastro e gerenciamento de pacientes e não cria relações com profissionais, disponibilidades ou agendamentos.

## Goals / Non-Goals

**Goals:**

- Persistir os dados mínimos necessários para identificar e contatar um paciente.
- Manter as validações e regras de integridade no backend.
- Disponibilizar operações de criação, consulta, edição e remoção de pacientes.
- Manter as respostas da API limitadas aos dados básicos previstos na spec.
- Manter a implementação preparada para futuras relações com outras entidades sem criá-las nesta change.

**Non-Goals:**

- Definir cadastro de profissionais, disponibilidades ou agendamentos.
- Criar relacionamentos entre pacientes e outras entidades.
- Coletar documentos de identificação, dados clínicos ou outros dados além de nome, telefone e e-mail.
- Criar autenticação, papéis, permissões ou novos fluxos de interface.
- Definir regras de histórico de atendimentos.

## Decisions

1. **Modelo mínimo de paciente**

   Cada paciente terá um identificador próprio gerado pelo sistema.

   O modelo inicial deverá possuir:

   - identificador próprio;
   - nome obrigatório;
   - telefone opcional;
   - e-mail opcional.

   O nome não poderá estar vazio nem conter somente espaços.

   Telefone, quando fornecido, poderá conter espaços, parênteses e hífens de formatação, terá entre 8 e 15 dígitos e poderá conter `+` somente no início. E-mail, quando fornecido, será validado pelo tipo nativo de e-mail do Xano após remover espaços externos.

   CPF e outros identificadores pessoais ficam fora desta change por não serem necessários ao escopo atualmente definido.

   **Alternativa considerada:** exigir um identificador civil ou tornar todos os dados de contato obrigatórios. Essa alternativa aumentaria a coleta de informações sem existir requisito de negócio que a justifique neste momento.

2. **Sem deduplicação por dados de contato**

   Nome, telefone e e-mail não serão tratados como chaves únicas.

   Pacientes diferentes poderão possuir dados coincidentes, como telefone compartilhado ou e-mail compartilhado.

   Cada registro será identificado pelo identificador próprio gerado pelo sistema.

   A API não rejeitará um cadastro somente porque nome, telefone ou e-mail também aparecem em outro registro.

   **Alternativa considerada:** impor unicidade de e-mail ou telefone. Essa alternativa poderia impedir cadastros legítimos e não existe regra de negócio aprovada que exija essa restrição.

3. **Validações no backend**

   As validações de campos, existência do paciente e integridade das operações deverão ser executadas no backend Xano.

   O frontend não deverá ser considerado responsável por garantir a integridade dos dados.

   As respostas da API deverão expor somente os dados previstos na spec:

   - identificador;
   - nome;
   - telefone;
   - e-mail.

   Campos internos da persistência que não sejam necessários ao consumidor da API não deverão ser expostos.

4. **Autorização fora do escopo desta change**

   Esta change não implementará autenticação, papéis ou permissões.

   Quando o projeto possuir um mecanismo de autenticação e autorização definido, as operações relacionadas a pacientes deverão respeitar as políticas de acesso correspondentes no backend.

   A ausência de autenticação nesta change não deverá ser interpretada como definição permanente de acesso público aos dados dos pacientes.

5. **Remoção física no escopo atual**

   Nesta change, a remoção de um paciente excluirá o registro persistido.

   Após a remoção, consultas utilizando aquele identificador deverão retornar paciente não encontrado.

   Essa decisão é válida para o escopo atual porque ainda não existem relações com agendamentos, atendimentos ou outros registros históricos.

   Antes da criação de funcionalidades que dependam do histórico do paciente, a estratégia de remoção deverá ser reavaliada.

   **Alternativa considerada:** utilizar inativação lógica desde o início. Essa alternativa adicionaria estado e regras de consulta sem existir requisito correspondente nesta etapa do projeto.

## Risks / Trade-offs

- **Contato compartilhado ou repetido:** a ausência de deduplicação pode permitir cadastros redundantes. O identificador próprio deverá ser utilizado como referência e uma política de deduplicação somente deverá ser criada caso surja uma regra de negócio que a justifique.

- **Exclusão irreversível:** a remoção física não preserva histórico. Como ainda não existem relacionamentos nesta change, a decisão é aceitável no escopo atual. Antes de relacionar pacientes a agendamentos ou atendimentos, a estratégia de retenção deverá ser reavaliada.

- **Dados pessoais:** pacientes possuem informações pessoais de identificação e contato. As respostas da API deverão ficar limitadas aos campos necessários e futuras regras de acesso deverão ser aplicadas no backend.

- **Validação de contato:** os critérios exatos para telefone e e-mail ainda precisam ser definidos antes da implementação. A ausência dessa definição poderá gerar comportamentos inconsistentes se cada operação utilizar critérios diferentes.

## Migration Plan

A implementação deverá criar a estrutura de persistência necessária para pacientes e as respectivas operações de API.

A tabela e as APIs existentes de `user` não deverão ser modificadas por esta change.

Não existe migração de pacientes existentes prevista, pois o projeto ainda não possui estrutura anterior para essa entidade.

Caso seja necessário desfazer esta change antes de existirem funcionalidades dependentes, as novas operações poderão ser removidas e a estrutura de pacientes poderá ser descontinuada de acordo com a situação dos dados existentes no ambiente.