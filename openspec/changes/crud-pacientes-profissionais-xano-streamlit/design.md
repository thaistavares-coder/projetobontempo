## Context

Consulte [proposal.md](./proposal.md) para motivação, escopo e limites. O cliente HTTP local em `frontend/services/listagens.py` implementa apenas GET de coleção e está desabilitado por padrão; as páginas de Pacientes e Profissionais ainda usam `frontend/services/database.py`, que também dá suporte a Especialidades e Consultas. Os arquivos `xano/table/` e `xano/api/` descrevem schemas e operações CRUD, mas não confirmam quais recursos estão publicados.

A Xano CLI confirmou o workspace `153318`, somente a branch `v1` marcada como live e `allow_push: false`. A CLI disponível lista workspaces e branches, mas não expõe comandos dedicados de leitura de tabelas ou APIs. A interface e a definição publicada das operações precisam ser comparadas por consulta autorizada antes de escolher qualquer alteração. Nenhuma operação remota faz parte desta etapa de planejamento.

## Goals / Non-Goals

**Goals:**

- Usar o contrato real confirmado como fonte para rotas, métodos, campos, validações e autenticação.
- Reutilizar o tratamento HTTP e os testes simulados existentes sem acoplar páginas ao transporte ou ao SQLite.
- Migrar o uso de dados de Pacientes e Profissionais para o Xano preservando os demais módulos locais durante a transição.
- Tornar explícitos os riscos de exibir ou alterar dados remotos e impedir testes destrutivos sobre registros existentes.

**Non-Goals:**

- Criar ou alterar schema, registros, endpoints publicados, autenticação, permissões ou credenciais nesta etapa.
- Inferir que os arquivos XanoScript locais estejam publicados ou que dados remotos sejam sintéticos.
- Introduzir catálogo de especialidades, associação N:N, consultas ou disponibilidade nesta mudança.
- Remover a persistência SQLite enquanto Especialidades e Consultas ainda dependem dela.

## Decisions

### Fazer reconciliação remota somente de leitura antes de definir endpoints a alterar

Registrar tabelas, campos, grupos, métodos, rotas, parâmetros, autenticação, validações e existência de registros sem copiar valores pessoais. Comparar essa evidência com XanoScript local antes de decidir se algum endpoint precisa ser criado, corrigido ou somente consumido. A definição local é referência de contrato pretendido, não prova de publicação.

Alternativa considerada: implementar diretamente todos os arquivos CRUD locais como se fossem o estado remoto. Rejeitada porque a divergência pode causar substituição de configuração, incompatibilidade ou exposição de dados.

O metadado `allow_push: false` e a ausência de branch não-live impedem presumir um fluxo de publicação seletiva. Qualquer plano de publicação deverá ser interrompido até que o responsável do workspace esclareça a restrição e autorize explicitamente a operação. Não usar `workspace push` amplo.

### Isolar operações HTTP em um serviço do domínio

Evoluir ou extrair o cliente HTTP existente para fornecer operações tipadas de coleção, item e escrita aos módulos de Pacientes e Profissionais. O serviço receberá a configuração externamente, aplicará timeout finito, verificará status e formato da resposta e exporá erros explícitos. As páginas não construirão URLs, cabeçalhos nem payloads diretamente.

Alternativa considerada: duplicar `requests` em cada página ou criar um cliente CRUD genérico sem contrato confirmado. A duplicação dificulta a consistência de erros; o cliente genérico anteciparia rotas e payloads que ainda não foram verificados.

Usar somente a configuração necessária ao contrato confirmado. Não acrescentar cabeçalho de autenticação ou token por suposição. Se a leitura remota revelar autenticação necessária, interromper até a autorização e configuração segura; não alterar permissões nem credenciais existentes.

### Tratar SQLite somente como legado de transição, nunca como backend permanente

As páginas migradas deixarão de chamar as funções SQLite. O serviço atual permanece temporariamente apenas porque Especialidades e Consultas ainda dependem dele; não serão acrescentadas funcionalidades SQLite. Changes subsequentes migrarão esses módulos para APIs Xano e, depois, removerão o serviço, a dependência e a inicialização SQLite da aplicação. O arquivo de dados existente não será apagado nem importado sem decisão específica de retenção/migração.

Alternativas consideradas: (1) manter SQLite como opção permanente ao lado do Xano; rejeitada porque contradiz a arquitetura oficial exclusivamente Xano; (2) apagar todo o serviço SQLite nesta mudança; rejeitada porque quebraria Especialidades e Consultas antes de suas migrações. A coexistência é somente uma etapa temporária e tem remoção total como requisito de conclusão da sequência de migração.

### Confirmar exclusões e usar somente registros sintéticos em testes remotos

Exigir confirmação explícita na interface antes de enviar DELETE. Testes automatizados usarão respostas simuladas. Testes remotos de escrita, quando autorizados, deverão criar registros sintéticos identificáveis para o ensaio e limitar PATCH/DELETE aos IDs retornados por essas criações. Não executar operações de escrita sobre registros desconhecidos ou preexistentes.

Alternativa considerada: validar DELETE selecionando um registro existente. Rejeitada pelo risco de perda de dados e pela falta de confirmação de que o workspace contém somente dados de teste.

### Preservar a diferença entre operação implementada e operação publicada

Uma página só poderá chamar uma operação cujo endpoint e contrato tenham sido confirmados. Implementar localmente serviço, formulários e testes simulados não autoriza chamada remota nem publicação. Habilitação real requer configuração externa e autorização operacional explícita; publicação requer ainda resolução do bloqueio `allow_push: false`.

Alternativa considerada: habilitar chamadas reais automaticamente ao configurar a URL base. Rejeitada porque a configuração não atesta a natureza dos dados, a autenticação nem a publicação dos endpoints.

## Risks / Trade-offs

- [O Xano contém dados pessoais ou registros que não foram identificados] → Não exibir respostas remotas nem executar escrita até confirmar acesso e natureza dos dados; não registrar payloads pessoais em logs ou testes.
- [A branch `v1` é live e `allow_push` está desabilitado] → Não publicar; solicitar orientação/autorização do responsável e validar um mecanismo seletivo antes de qualquer alteração.
- [Rotas, métodos ou campos remotos divergem dos arquivos locais] → Usar o inventário remoto aprovado como fonte do contrato e atualizar XanoScript somente após autorização, sem push amplo.
- [DELETE de paciente/profissional poderá conflitar com relações futuras] → Exigir confirmação na interface; não remover registros preexistentes em testes; revisar política de retenção e dependências antes de habilitar a operação remota.
- [A migração parcial deixa SQLite no projeto] → Limitar o uso residual a Especialidades e Consultas, documentar o caráter transitório e não remover o banco local.
- [Falhas de rede ou respostas inesperadas podem parecer sucesso] → Validar resposta e apresentar erro explícito; nunca converter falha em lista vazia ou sucesso.

## Migration Plan

1. Obter inventário remoto somente de leitura, com método seguro para não revelar dados pessoais; reconciliar contratos e registrar o estado atual.
2. Confirmar quais métodos já existem, quais podem ser consumidos e quais exigiriam alteração remota. Não criar schema se as tabelas existentes forem suficientes.
3. Implementar e testar localmente o serviço HTTP e as páginas com mocks, mantendo a configuração real desabilitada.
4. Após autorização específica, validar chamadas remotas em `v1` apenas se houver endpoint confirmado e estratégia segura de dados sintéticos; não publicar novas definições enquanto `allow_push` estiver bloqueado.
5. Migrar Especialidades e Consultas para APIs Xano em Changes subsequentes, sem novos recursos SQLite e sem alternância permanente de backend.
6. Após a migração de todas as páginas, remover serviço, dependências e inicialização SQLite; preservar o arquivo de banco local até uma decisão/autorização específica de retenção ou migração. Nenhuma exclusão de dados locais está incluída nesta mudança.

## Open Questions

- Como obter um inventário remoto de tabelas e endpoints sem `workspace pull` e sem expor registros pessoais?
- Quais rotas, métodos, esquemas de entrada/saída e controles de acesso estão efetivamente publicados em `v1`?
- O responsável do workspace autoriza chamadas reais de leitura e, separadamente, escritas sintéticas? Como será resolvido `allow_push: false` sem publicação ampla?
- Existe alguma relação remota já criada entre pacientes/profissionais e dados que exija bloquear DELETE?
