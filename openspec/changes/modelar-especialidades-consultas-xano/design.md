## Context

Consulte [proposal.md](./proposal.md) e as deltas em `specs/`. Nos arquivos do repositório, `paciente` e `profissional` possuem chave primária inteira; `profissional.especialidade` é texto opcional. Os GETs locais de profissionais expõem esse campo textual. Não foram encontradas definições Xano versionadas para as quatro tabelas novas, exemplos de FKs ou índices únicos compostos. Os arquivos locais não comprovam publicação, configuração, dados ou restrições no Xano de destino.

A Change `revisar-escopo-modelo-clinica` aprova a relação N:N Médico–Especialidade, com zero vínculos permitidos durante a transição e exigência de vínculo para agendar; outras cardinalidades e regras de retenção continuam pendentes. `integrar-listagens-xano-streamlit` preserva o campo textual e o contrato GET atual. Ambas permanecem intactas e são dependências de domínio/compatibilidade, não autorização para alterar endpoints. Esta Change propõe o modelo abaixo; decisões ainda marcadas como pendentes bloqueiam sua implementação até aprovação.

## Goals / Non-Goals

**Goals:**

- Propor tipos conceituais, PKs, FKs, cardinalidades, unicidade e invariantes para as quatro tabelas.
- Separar a validação da agenda e da associação médico-especialidade dos controles da interface.
- Manter dados e contratos atuais compatíveis, sem migração automática do texto legado.
- Delimitar questões que precisam de aprovação e uma sequência segura de Changes futuras.

**Non-Goals:**

- Criar tabelas ou endpoints, executar XanoScript, migrar dados ou confirmar o ambiente publicado.
- Definir conteúdo clínico, prontuários, registros de atendimento, autenticação ou login.
- Tratar a validação da interface como controle de integridade ou segurança.

## Decisions

### Modelo físico proposto para avaliação

Todos os `id` são propostos como `int` gerado pelo Xano, chave primária independente e sem reutilização. Os tipos abaixo são conceituais e seguem os tipos visíveis nos arquivos locais quando há equivalência; a compatibilidade exata com Xano deverá ser confirmada antes de gerar XanoScript.

| Tabela | Atributos propostos | PK/FK e restrições |
|---|---|---|
| `especialidade` | `id int`; `nome text` obrigatório; `nome_normalizado text` derivado no backend | PK em `id`; `nome_normalizado` único após trim e conversão para minúsculas, preservando acentos; não excluir fisicamente se houver vínculos/consultas |
| `profissional_especialidade` | `id int`; `profissional_id int`; `especialidade_id int` | PK em `id`; FKs para `profissional.id` e `especialidade.id`; unicidade composta de `(profissional_id, especialidade_id)` para impedir duplicidade |
| `status_consulta` | `id int`; `codigo text` obrigatório; `nome text` obrigatório; `ocupa_horario bool` obrigatório | PK em `id`; `codigo` único e estável; valores iniciais aprovados abaixo; transições de status para APIs permanecem fora desta Change |
| `consulta` | `id int`; `paciente_id int`; `profissional_id int`; `especialidade_id int`; `status_consulta_id int`; `inicio_em timestamp`; `fim_em timestamp` | PK em `id`; FKs obrigatórias para `paciente.id`, `profissional.id`, `especialidade.id` e `status_consulta.id`; índices de consulta por FKs e `inicio_em`; intervalo no mesmo dia local, com `fim_em` posterior a `inicio_em` |

O uso de timestamps evita depender de um tipo separado para data e hora. `America/Sao_Paulo` é a referência proposta para interpretar os horários locais da clínica; o fuso e sua conversão para os timestamps deverão ser confirmados antes da implementação. `bool`, `timestamp`, a geração de `nome_normalizado` e a sintaxe de restrições ainda precisam ser confirmados com a versão e o ambiente Xano de destino. `ocupa_horario` representa somente uma regra do catálogo de status, não dado clínico.

### Cardinalidades propostas

- `profissional` 0..N — `profissional_especialidade` — 1 `especialidade`: cada linha associativa aponta para exatamente um profissional e uma especialidade; cada lado pode ter vários vínculos.
- A cardinalidade mínima aprovada para esta transição é 0..N especialidades por profissional. Uma consulta, por exigir especialidade, somente pode ser marcada para médico que tenha vínculo com a especialidade escolhida.
- `paciente` 0..N `consulta`; cada `consulta` tem exatamente 1 paciente.
- `profissional` 0..N `consulta`; cada `consulta` tem exatamente 1 profissional.
- `especialidade` 0..N `consulta`; cada `consulta` tem exatamente 1 especialidade, e essa combinação deve existir em `profissional_especialidade`.
- `status_consulta` 0..N `consulta`; cada `consulta` tem exatamente 1 status atual.
- Esta Change não cria relação com prontuário ou registro clínico; consulta agendada não depende deles.

### Integridade, unicidade e exclusão

- Validar FKs no backend e, se o Xano suportar constraints declarativas adequadas, também no banco. Nenhuma associação ou consulta pode ser gravada parcialmente.
- Aplicar unicidade ao par profissional-especialidade. A forma física do índice composto deve ser validada no Xano; um `id` associativo sozinho não impede duplicidade.
- Comparar especialidades por `nome_normalizado`, derivado com trim e minúsculas, mantendo acentos; índice único e consistência do valor derivado devem ser verificados no backend/Xano.
- Aplicar unicidade de código do status. Valores iniciais aprovados para `status_consulta`: `agendada`, `confirmada`, `realizada`, `cancelada` e `nao_compareceu`; a tabela armazena somente o status atual, sem histórico de transição nesta modelagem.
- Consultas devem ter índices úteis para `profissional_id`, `inicio_em` e status sem assumir que esses índices, isoladamente, evitam sobreposição.
- Não usar cascata destrutiva. Exclusões de médico/paciente/especialidade/status com dependentes devem ser bloqueadas ou seguir política de retenção aprovada. Preferir desativar especialidade/status quando houver referências.
- A validação de horário deve ser no backend, por intervalo `[inicio_em, fim_em)` no mesmo dia local, interpretado pela referência proposta `America/Sao_Paulo`. `fim_em` deve ser posterior a `inicio_em`. Horários consecutivos cujo fim coincide com o início seguinte são permitidos; sobreposição entre intervalos de mesmo médico é conflito se ambos os status ocupam horário.
- Para o seed inicial, `agendada` e `confirmada` ocupam horário; `realizada`, `cancelada` e `nao_compareceu` liberam o horário. A regra de transições de status permanece para uma Change de APIs/regras.
- Prevenir corrida entre duas criações simultâneas exige mecanismo atômico/serialização ou constraint equivalente. A disponibilidade desse mecanismo no Xano precisa ser comprovada; se não houver forma segura de garanti-lo, a regra não deve ser declarada implementada.

### Compatibilidade com `profissional.especialidade`

1. Manter o campo atual, seus valores e a forma de resposta dos GETs e demais endpoints existentes.
2. Criar `especialidade` e `profissional_especialidade` sem popular vínculos a partir do texto automaticamente.
3. Planejar uma reconciliação em Change futura separada, com relatório de valores distintos, mapeamento explícito aprovado, revisão dos não correspondentes, contagem antes/depois, backup e rollback.
4. Não remover nem alterar o campo ou o contrato atual até consumidores serem migrados em Change de API própria. A tabela associativa não torna o campo textual automaticamente sincronizado ou fonte de verdade.

### Dependências e ordem de implementação futura

1. Inspecionar o ambiente Xano de destino autorizado, comparar inventário publicado com arquivos versionados e confirmar permissões, tipos, FKs, índices compostos e transações. A auditoria somente de leitura identificou a branch `v1` como live e não encontrou branch de desenvolvimento visível.
2. Verificar com a documentação da versão Xano de destino suporte a tipos, FKs, índices únicos compostos e garantia atômica; a cardinalidade N:N e o mínimo 0 durante a transição aprovados nesta Change complementam, sem modificar, a Change de revisão de escopo.
3. Bloqueio de publicação identificado: a única branch remota reportada foi `v1`, marcada como live, sem branch de desenvolvimento visível. Não criar nem publicar tabelas nessa branch nesta etapa; a implementação requer destino não-live isolado e autorizado.
4. O `workspace push --dry-run` do estado local identificou atualizações não relacionadas nas tabelas existentes: `profissional`, função `validar_telefone_paciente`, grupo de API `Profissionais` e três endpoints existentes (PATCH de paciente, POST e PATCH de profissional). Também reportou referências não resolvidas em addons de `user` e funções de exemplo. O dry-run não publicou alterações; não executar push amplo enquanto esse diff não estiver explicado e isolado.
5. Criar Change de esquema aditiva e reversível: catálogo e vínculo, catálogo de status com seed aprovado, depois consultas; preservar PKs e valores atuais.
6. Criar Change de APIs/regras: CRUD de catálogo/vínculos/consultas, transições de status, verificação da especialidade do médico e conflito concorrente; manter endpoints antigos.
7. Rever contrato GET de profissionais para especialidades relacionais somente em Change separada, mantendo a compatibilidade durante migração.
8. Alterar Streamlit/integrar endpoints somente após confirmação de segurança, APIs publicadas e dados de demonstração seguros. Nenhuma etapa desta Change habilita integração.

### Riscos e segurança

- [Arquivos locais divergirem do Xano publicado] → fazer inventário e backup no ambiente autorizado antes de qualquer DDL; não alegar que tabelas ausentes localmente não existem no remoto.
- [A branch remota identificada é live e o dry-run inclui mudanças em recursos existentes] → não direcionar publicação a `v1` nem executar push amplo; exigir branch/workspace não-live autorizado, escopo aditivo isolado e novo dry-run sem alterações inesperadas antes de qualquer publicação.
- [Vínculos inferidos automaticamente criarem associações erradas] → não migrar `profissional.especialidade`; exigir mapeamento explícito e rollback.
- [Restrição composta ou transação não ser suportada da forma esperada] → validar com documentação e no workspace de desenvolvimento, sem alterar produção; bloquear a implementação se não houver integridade contra concorrência.
- [Ausência de login expor dados de pacientes ou consultas] → limitar demonstração a dados fictícios, avaliar e aprovar controles de acesso no backend e no ambiente antes de publicar ou integrar; não considerar acesso local ou configuração do frontend como salvaguarda suficiente.
- [Referências impedirem remoções ou causarem perda de histórico] → nenhuma cascata implícita; decidir retenção e exclusão antes das APIs.
- [A integração de listagens tratar `especialidade` como texto] → preservar contrato e campo legado até consumidores e API terem Change de transição própria.

## Open Questions

As respostas abaixo não alteram as quatro tabelas especificadas, mas são pré-condições para Changes futuras de APIs, agenda ou exposição; não devem ser decididas silenciosamente:

1. Quais transições entre os status aprovados serão permitidas? A tabela proposta guarda apenas o status atual, sem histórico; transições futuras exigem aprovação numa Change de APIs/regras.
2. O grupo confirma `America/Sao_Paulo` como fuso da clínica e a política de conversão/armazenamento dos campos `inicio_em` e `fim_em` como timestamps?
3. A agenda futura também validará disponibilidade do médico? Nenhuma tabela/estrutura de disponibilidade correspondente foi encontrada nos arquivos Xano versionados; essa capacidade requer modelagem própria.
4. Quais controles de acesso aprovados protegerão APIs de pacientes e consultas, considerando a ausência de login? Quem autoriza a publicação e habilitação da integração?

Até essas respostas, transições de status, fuso da API, validação de disponibilidade e salvaguardas para exposição permanecem fora desta modelagem. Exclusões de registros referenciados ficam restritas, sem cascata, até aprovação de política específica. A compatibilidade técnica das constraints no Xano também deve ser demonstrada; em caso negativo, revisar o modelo antes de aplicá-lo.
