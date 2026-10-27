## Context

Consulte [proposal.md](./proposal.md) para a motivação e o escopo. Esta Change acrescentou listagens GET à aplicação Streamlit multipágina. A Change `crud-pacientes-profissionais-xano-streamlit` posteriormente substituiu a experiência dessas duas páginas por operações CRUD através do cliente Xano. As decisões GET-only abaixo descrevem a fase inicial e não restringem a Change CRUD. Os arquivos XanoScript e as respostas de leitura não comprovam, por si sós, que a segurança do ambiente esteja adequada.

A Change `revisar-escopo-modelo-clinica` está ativa. Ela não é dependência desta integração: seu escopo de revisão não altera as listagens existentes, e esta Change não altera seus artefatos nem antecipa relacionamentos de especialidade, consultas ou prontuários.

## Goals / Non-Goals

**Goals:**

- Isolar configuração, chamadas GET, parsing e erros HTTP num módulo compartilhado reutilizável.
- Preservar a navegação, estilos e estrutura das páginas, mudando somente os dados da tabela e estados relacionados à listagem.
- Tornar explícitos os limites de segurança e criar testes sem rede e sem dados reais.

**Non-Goals:**

- Acrescentar uma API genérica de escrita, autenticação ou operações de usuário.
- Implementar o catálogo de especialidades ou alterar o campo textual devolvido para Profissionais.
- Tratar endpoints testados localmente como confirmação da segurança ou da configuração de produção.

## Decisions

### Centralizar o cliente HTTP para a fase inicial de listagem

Na fase inicial, criar um módulo sob `frontend/services/` que receba/configure a URL completa de cada listagem, aplique timeout, execute GET, verifique status e valide que a resposta é uma lista de objetos com os campos esperados. A Change CRUD posterior define o cliente e as rotas usados pelas operações atuais das páginas.

Alternativa considerada: duplicar chamadas e parsing nas páginas. Foi rejeitada por duplicar tratamento de falhas e dificultar testes. A limitação a GET pertence somente a esta fase inicial; não limita as operações definidas pela Change CRUD.

### Usar configuração externa para a camada GET inicial

O cliente GET desta etapa usa `XANO_PACIENTES_URL` e `XANO_PROFISSIONAIS_URL` para URLs completas. Essa configuração pertence à implementação GET inicial; a Change CRUD especifica as variáveis e a habilitação usadas atualmente pelas páginas. Não adicionar token ou credencial; qualquer requisito de acesso descoberto interrompe a habilitação até revisão de segurança.

Alternativa considerada: fixar a base/rotas do Xano no módulo ou incluir `.env` com valores reais. Foi rejeitada porque dificulta ambientes distintos e pode versionar configuração de execução. Um exemplo versionado, se necessário, deverá manter os valores vazios e ser explicitamente ilustrativo.

### Usar `requests` com timeout explícito e declarar dependência direta

Adicionar `requests` ao manifesto se a implementação importar essa biblioteca diretamente. A chamada terá timeout finito (o valor exato ficará no código e nos testes) e converterá timeout, falha de conexão, erro HTTP, JSON inválido e coleção/registro incompatível em erros de leitura controlados.

Alternativa considerada: usar `urllib` da biblioteca padrão para evitar dependência. `requests` foi preferido pela ergonomia de status/JSON e pela compatibilidade com simulação de transporte nos testes; a dependência deverá ser direta, não presumida por dependência transitiva do Streamlit.

### Cachear as listagens da fase inicial

Na implementação GET inicial, cachear cada listagem por até 60 segundos e oferecer atualização explícita. Essa decisão descreve o serviço GET original; o comportamento das páginas após a integração CRUD é definido pela Change `crud-pacientes-profissionais-xano-streamlit`.

Alternativa considerada: consultar em todo rerun ou cache sem ação de atualização. A primeira opção gera tráfego desnecessário; a segunda não atende à necessidade de atualizar uma lista antes da expiração.

### Testar sem chamadas de rede reais

Usar `unittest` e mocks de transporte para respostas válidas com dados sintéticos, coleção vazia, erro HTTP, timeout, falha de conexão, JSON inválido e shape inesperado. Não consultar endpoints durante testes, não gravar respostas do ambiente real e não usar dados pessoais reais ou clínicos.

Alternativa considerada: testes de integração contra o Xano. Foram rejeitados para esta Change por dependerem de rede/dados externos e pelo requisito de comprovar que os registros são fictícios e o ambiente está adequadamente restrito antes de expor qualquer resposta.

### Manter a integração GET inicial desabilitada por padrão

As funções de listagem desta fase recusam chamadas enquanto `XANO_LISTAGENS_ENABLED` não estiver explicitamente definido como `true`. Esse sinalizador é uma trava operacional de frontend, não um controle de acesso nem evidência de que o Xano está seguro. A integração CRUD posterior tem configuração própria e não altera permissões ou credenciais do Xano. A tarefa de segurança 1.2 permanece pendente: não considerar a existência de GET bem-sucedido evidência de que os registros são fictícios ou de que o acesso está adequadamente restrito.

Alternativa considerada: habilitar chamadas automaticamente quando as URLs estiverem presentes. Foi rejeitada porque a natureza dos dados foi confirmada como teste, mas a restrição de acesso aos endpoints ainda não foi verificada.

## Risks / Trade-offs

- [Endpoints GET podem expor registros a qualquer pessoa sem autenticação] → Manter `XANO_LISTAGENS_ENABLED` ausente/falso até confirmar registros fictícios, restrição adequada e autorização explícita; não incluir testes vivos nem dados no repositório.
- [API pode retornar shape diferente do código local] → Validar cada resposta em runtime e mostrar falha explícita, sem fallback de sucesso ou lista vazia.
- [Cache mantém dados antigos por até 60 segundos] → Expor atualização manual por módulo e documentar o prazo máximo.
- [Variáveis de ambiente podem não ser configuradas na execução do Streamlit] → Detectar ausência antes da rede e exibir instrução clara; nunca embutir URL como fallback.
- [A spec consolidada atualmente diz que a primeira entrega não faz HTTP] → A delta altera explicitamente esse contrato preservando seus cenários e permite somente os dois GETs, sem modificar os limites de segurança, de escrita ou de integração futura.

## Migration Plan

Não há migração de Xano nesta etapa. O cliente e os testes GET registram a primeira fase de integração; a Change CRUD posterior define o comportamento integrado atual de Pacientes e Profissionais. A verificação de segurança continua pendente conforme a tarefa 1.2. Nenhuma destas Changes autoriza alterar dados, tabelas, endpoints, permissões ou credenciais remotas.
