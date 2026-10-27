## 1. Atualização da documentação

- [x] 1.1 Atualizar `AGENTS.md` para registrar Python/Streamlit como frontend, Xano HTTP como backend e a regra de não acessar o banco diretamente; verificar que as orientações de arquitetura e segurança refletem essa divisão.
- [x] 1.2 Atualizar `docs/project-overview.md` para documentar o frontend Streamlit e sua comunicação com as APIs HTTP do Xano; revisar a seção de arquitetura para confirmar que não conflita com o escopo nem com o domínio existente.

## 2. Estrutura inicial do frontend

- [x] 2.1 Confirmar a versão Python suportada no ambiente de execução e definir um manifesto mínimo de dependências para Streamlit; verificar que somente dependências necessárias foram declaradas e que a instalação e a inicialização local funcionam.
- [x] 2.2 Criar a estrutura `frontend/` com ponto de entrada para Início e páginas Pacientes e Profissionais; verificar que os arquivos previstos existem e que a aplicação inicia pelo comando documentado.
- [x] 2.3 Implementar a navegação multipágina sem chamadas HTTP nem operações de dados nesta entrega inicial; verificar visualmente que Início, Pacientes e Profissionais podem ser abertos e que as opções de navegação permanecem disponíveis.

## 3. Limites de integração e segurança

- [x] 3.1 Manter URLs e credenciais fora do código versionado e evitar valores sensíveis em exemplos de configuração; verificar os arquivos novos e as regras de exclusão de configurações locais antes de concluir.
- [x] 3.2 Registrar como bloqueios para uma integração futura a confirmação da URL base das APIs, os requisitos oficiais de autenticação e a análise do valor aparentemente sensível em `xano/api/autentication/autentication.xs`; verificar que nenhuma chamada ou credencial foi adicionada enquanto essas pendências não forem resolvidas.
- [x] 3.3 Confirmar que eventual integração posterior usará apenas endpoints existentes de pacientes e profissionais; verificar que esta entrega não adiciona operações de agendamento/disponibilidade, não modifica `xano/` e não altera as especificações consolidadas.

## 4. Verificação da entrega

- [x] 4.1 Executar as verificações locais da aplicação e revisar a navegação nas três páginas; confirmar também que as páginas não simulam sucesso nem dados de API.
- [x] 4.2 Validar a Change OpenSpec e revisar `git status`/`git diff`; confirmar que as únicas alterações estão no frontend planejado e na documentação prevista, sem mudanças em `xano/` ou `openspec/specs/pacientes/` e `openspec/specs/profissionais/`.
