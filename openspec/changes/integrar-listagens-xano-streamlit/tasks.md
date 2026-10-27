## 1. Pré-condições de segurança e configuração

- [x] 1.1 Manter chamadas reais desabilitadas por padrão, exigir `XANO_LISTAGENS_ENABLED=true` para qualquer GET e confirmar em teste que URLs configuradas não contornam o bloqueio.
- [ ] 1.2 Antes de habilitar no ambiente de demonstração, confirmar e registrar que os dados são exclusivamente fictícios, que o acesso aos endpoints está adequadamente restrito e que o grupo autorizou explicitamente a habilitação. Esta confirmação continua pendente; manter o sinalizador ausente/falso até sua conclusão.
- [x] 1.3 Documentar `XANO_PACIENTES_URL` e `XANO_PROFISSIONAIS_URL` como configuração externa das URLs completas dos GETs; verificar que não há URLs operacionais, tokens ou credenciais embutidos em código ou arquivos versionados.

## 2. Cliente HTTP reutilizável

- [x] 2.1 Adicionar o módulo compartilhado de listagens sob `frontend/services/` e declarar diretamente a dependência HTTP escolhida em `frontend/requirements.txt`; verificar que o cliente expõe somente leitura GET, aplica timeout finito e valida status, JSON e campos de cada coleção.
- [x] 2.2 Tratar configuração ausente, integração desabilitada, erro HTTP, timeout, falha de conexão, JSON inválido e estrutura inesperada com erros explícitos; verificar que nenhum caso de falha retorna lista vazia ou registros fictícios como fallback.
- [x] 2.3 Criar testes automatizados com transporte simulado para sucesso com registros sintéticos, lista vazia, erro HTTP, timeout, falha de conexão, JSON inválido e estrutura incompatível; verificar que a suíte não faz chamadas de rede nem utiliza dados pessoais ou clínicos reais.

## 3. Exibição das listagens Streamlit (fase GET inicial)

- [x] 3.1 Na fase GET inicial, atualizar `frontend/pages/1_Pacientes.py` para usar o cliente compartilhado, manter layout/colunas e controles de busca e criação desabilitados, e apresentar estados de carregamento, erro e lista vazia; a Change CRUD posterior substitui o estado final desses controles.
- [x] 3.2 Na fase GET inicial, atualizar `frontend/pages/2_Profissionais.py` para usar o mesmo cliente e manter `especialidade` textual; verificar estados de lista vazia e erro e que não se cria catálogo ou relacionamento. A Change CRUD posterior habilita as operações previstas para Profissionais.
- [x] 3.3 Reutilizar resultados por até 60 segundos e oferecer atualização explícita por módulo; verificar que reruns dentro do prazo não repetem GET sem necessidade e que atualizar invalida apenas o cache correspondente.
- [x] 3.4 Atualizar `frontend/README.md` com a configuração externa, execução, atualização/cache e mensagens de erro; verificar que instruções não incluem segredos nem valores de URL operacional.

## 4. Verificação final da integração

- [x] 4.1 Executar testes automatizados e smoke test local das três páginas com APIs simuladas ou configuração ausente; verificar navegação, identidade visual, colunas e ausência de escritas remotas nesta fase GET. Os fluxos de escrita simulados e a interface CRUD são cobertos pela Change posterior.
- [x] 4.2 Revisar `git diff` e `git status`; verificar que a implementação se limita ao frontend, testes, documentação e artefatos desta Change, sem alterar Xano, dados ou a Change `revisar-escopo-modelo-clinica`.
