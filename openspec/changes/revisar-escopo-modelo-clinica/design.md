## Context

Consulte [proposal.md](./proposal.md) para o motivo e o limite desta Change. As deltas em `specs/` definem os requisitos propostos; este design registra como separar fatos locais, decisões aprovadas e questões que continuam sujeitas à validação do grupo.

Evidências observadas no workspace:

- `xano/table/` contém `user`, `paciente` e `profissional`. As tabelas de paciente e profissional têm somente ID e dados básicos; `profissional.especialidade` é texto opcional. Não foram encontradas tabelas de especialidade, consulta, status de consulta, prontuário ou registro de atendimento, nem chaves estrangeiras ou índices de unicidade para essas relações.
- `xano/api/` contém endpoints CRUD de pacientes e profissionais e endpoints CRUD de `user` no grupo localmente nomeado `Autentication`. Os arquivos examinados não declaram login, criação de sessão, papel, nem referência aos usuários nos endpoints de pacientes e profissionais. Isso descreve apenas os arquivos locais e não comprova a configuração ou a exposição do ambiente Xano publicado.
- As tabelas locais declaram `auth = false`; isso não comprova controles efetivos de acesso nas APIs publicadas ou na infraestrutura.
- As especificações consolidadas de pacientes e profissionais descrevem CRUD e dados pessoais básicos. Profissionais ainda permitem especialidade em texto livre. A entrega inicial tinha Início, Pacientes e Profissionais sem chamadas HTTP e tabelas vazias; uma Change posterior planeja/implementa listagens GET condicionais, mantendo-as desabilitadas por padrão até as verificações de segurança e autorização.
- O arquivo de referência PDF indicado não está disponível no workspace. A Change usa como fonte para as decisões aprovadas o pedido do grupo e registra as inferências como pendentes.

## Goals / Non-Goals

**Goals:**

- Consolidar no OpenSpec o escopo funcional aprovado e um contrato conceitual para as relações clínicas.
- Tornar verificáveis os bloqueios de modelagem, integridade e proteção de dados que precisam de aprovação antes de mudanças físicas ou de API.
- Distinguir o que existe nos arquivos locais, o que foi aprovado pelo grupo e o que ainda é hipótese.

**Non-Goals:**

- Atualizar `docs/project-overview.md` ou `docs/domain-model.md` antes de o grupo aprovar as decisões pendentes.
- Alterar Xano, banco, dados, endpoints, frontend, autenticação ou configuração publicada.
- Presumir que a notação “PRONTUARIO 1 REGISTRO_ATENDIMENTO” defina cardinalidade física sem confirmação; a relação N:N Médico–Especialidade está aprovada, mas suas restrições físicas ainda precisam de validação.

## Decisions

### Separar entidade conceitual de evidência de implementação

As tabelas e endpoints são descritos como arquivos presentes no repositório, não como recursos confirmados no ambiente publicado. A Change não cria estrutura física; cada futura implementação deverá validar o ambiente e mapear dados e dependências antes de migração.

Alternativa considerada: tratar os arquivos Xano locais como prova de que APIs estão implantadas. Isso foi rejeitado porque o workspace não confirma publicação, permissões ou autenticação do ambiente alvo.

### Tratar decisões aprovadas como contrato e cardinalidades incertas como bloqueios

O escopo sem login, os cinco módulos, o médico como único tipo de profissional, a relação N:N Médico–Especialidade com zero vínculos possíveis durante a transição, a exigência de vínculo para agendar consultas, o prontuário opcional por paciente, o registro clínico associado à consulta realizada e a localização dos campos clínicos em REGISTRO_ATENDIMENTO são decisões aprovadas pelo grupo. A quantidade de registros por prontuário, o catálogo e as transições de STATUS_CONSULTA e as políticas de retenção/exclusão ficam pendentes de confirmação.

Como hipótese para revisão, um prontuário longitudinal tende a conter múltiplos registros. A especificação exige que essa hipótese seja aprovada, não a transforma em restrição de banco nesta Change.

Alternativa considerada: escolher unilateralmente cardinalidades usuais de agenda clínica. Isso foi rejeitado porque a cardinalidade de prontuário–registro, o histórico de status e a retenção clínica ainda têm impacto de domínio e integridade; a cardinalidade Médico–Especialidade já foi aprovada pelo grupo.

### Manter diagnóstico e conteúdo clínico no registro de atendimento

CONSULTA representa a agenda e o estado da consulta, enquanto REGISTRO_ATENDIMENTO contém diagnóstico, anotações clínicas e conduta. Uma consulta apenas agendada pode existir sem prontuário ou registro; uma consulta realizada pode ter no máximo um registro próprio conforme decisão do grupo.

Alternativa considerada: colocar campos clínicos em CONSULTA por simplicidade. Isso duplica semânticas e acopla agendamento a documentação clínica, contrariando as decisões aprovadas.

### Não inferir autenticação nem remover artefatos de usuário

Os endpoints locais de `user` parecem operações genéricas de cadastro, consulta, edição e remoção. Nenhum fluxo de login, papel ou uso desses endpoints pelos módulos de pacientes/profissionais foi identificado. A versão aprovada não inclui gerenciamento de usuários ou login; a tabela e os endpoints existentes permanecem intocados até uma Change específica decidir seu destino.

Alternativa considerada: remover `user` por estar fora do escopo. Isso foi rejeitado porque a restrição proíbe excluir entidades existentes e a presença de endpoints pode ter dependências externas ainda não verificadas.

### Bloquear exposição clínica até aprovação de salvaguardas

Como o escopo não inclui login, a futura persistência ou exposição de prontuários precisa de análise aprovada de confidencialidade, controle de acesso, exposição de APIs, auditoria e retenção antes de ser habilitada. Esta decisão não introduz login nem escolhe um controle compensatório específico; a ausência de login não significa acesso público.

Alternativa considerada: adiar qualquer análise de segurança até a integração frontend–backend. Isso foi rejeitado porque dados clínicos podem ser expostos por APIs independentemente do frontend e as regras de segurança devem ser tratadas no backend.

## Risks / Trade-offs

- [A ausência de login pode permitir acesso indevido a dados clínicos se endpoints estiverem publicamente acessíveis] → Não expor ou integrar prontuários até que salvaguardas sem login sejam definidas, validadas e aprovadas; confirmar separadamente as políticas do ambiente Xano.
- [Cardinalidades ainda ambíguas podem causar duplicidade, órfãos ou migração destrutiva] → Obter decisão explícita sobre prontuário–registro, consulta–status, consulta–registro e exclusões; implementar Médico–Especialidade como N:N com integridade validada e consulta condicionada a vínculo existente.
- [O campo de especialidade em texto livre permite grafias inconsistentes e não identifica uma especialidade referenciada] → Tratar o catálogo e a conversão dos valores existentes numa Change de modelo/migração aprovada.
- [Regras atuais de exclusão de paciente e profissional não consideram dados dependentes futuros] → Definir retenção e comportamento de exclusão antes de criar referências clínicas; impedir cascatas implícitas.
- [Os arquivos locais podem divergir do Xano publicado] → Inspecionar o ambiente de destino e planejar backup, migração reversível e reconciliação antes da implementação.
- [Há metadado local com aparência de credencial no grupo Xano de autenticação] → Não reproduzir o valor; confirmar se está ativo e, se necessário, tratar sua rotação em fluxo seguro antes de publicar ou usar o grupo.

## Migration Plan

Não há migração nesta Change. Após aprovação das decisões, esta Change atualizará a documentação do domínio e da visão geral. A implementação deverá ocorrer em Changes independentes: (1) definir esquema, restrições e migração de dados Xano, preservando dados e referências existentes; (2) especificar e implementar regras e APIs para especialidades, consultas, status, prontuários e registros com salvaguardas aprovadas; (3) atualizar o frontend e integrar somente depois de validar endpoints, ambiente e proteção de dados.

Cada etapa deverá ter critérios de reversão próprios. Não remover `user`, `paciente` ou `profissional`; qualquer transformação de especialidade em catálogo ou adição de relações deve preservar IDs e dados existentes, com plano de rollback aprovado antes da execução.

## Pontos para aprovação do grupo

- `PRONTUARIO 1 REGISTRO_ATENDIMENTO`: confirmar se significa um prontuário para vários registros (hipótese compatível com histórico) ou outra cardinalidade.
- Médico–Especialidade: relação N:N aprovada, com zero ou mais vínculos por médico durante a transição; exigir vínculo entre médico e especialidade para agendamento e validar FKs e unicidade do par na Change de implementação.
- `STATUS_CONSULTA`: aprovar valores, status inicial, transições, possibilidade de histórico e cardinalidade.
- Exclusão/retenção: aprovar o comportamento para paciente, médico, consulta e registro clínico quando houver dependências.
- Sem login: aprovar controles de acesso/confidencialidade adequados antes de dados clínicos serem persistidos ou servidos.
