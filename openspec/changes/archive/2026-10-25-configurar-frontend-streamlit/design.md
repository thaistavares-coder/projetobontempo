## Context

Consulte [proposal.md](./proposal.md) para a motivação e [specs/interface-web/spec.md](./specs/interface-web/spec.md) para o contrato observável.

O repositório atualmente contém arquivos XanoScript em `xano/api/` e `xano/table/`, mas não contém aplicação Python, manifesto de dependências nem diretório `frontend/`. As APIs identificadas para esta Change são as listagens de pacientes (`GET /pacientes`) e profissionais (`GET /profissionais`), além das operações por identificador já declaradas nos respectivos grupos. Os arquivos locais não determinam a URL base implantada nem os requisitos de autenticação do ambiente alvo.

## Goals / Non-Goals

**Goals:**

- Preparar uma aplicação Streamlit com ponto de entrada e páginas para Início, Pacientes e Profissionais.
- Definir o limite da futura integração HTTP com Xano, sem acoplar a interface ao banco de dados.
- Separar configuração do ambiente e segredos do código versionado.
- Registrar os bloqueios necessários antes de habilitar chamadas às APIs.

**Non-Goals:**

- Implementar chamadas às APIs ou operações de cadastro, consulta, edição e remoção de pacientes ou profissionais nesta entrega inicial.
- Criar ou alterar endpoints, tabelas ou arquivos Xano.
- Implementar agendamentos, disponibilidades ou autenticação ainda não confirmada.
- Alterar os requisitos consolidados de pacientes ou profissionais.

## Decisions

### Usar a estrutura multipágina nativa do Streamlit

O ponto de entrada será `frontend/app.py`, responsável pela página Início. As páginas Pacientes e Profissionais ficarão em `frontend/pages/`, seguindo a navegação multipágina do Streamlit.

Alternativa considerada: construir navegação própria em uma única página. A estrutura nativa é preferida por ser simples, evitar roteamento customizado e manter as três áreas separadas.

### Centralizar chamadas HTTP e configuração

Quando a integração for autorizada, o acesso às APIs ficará concentrado em um cliente compartilhado sob `frontend/services/`, enquanto os dados de configuração serão obtidos do ambiente de execução. A configuração não terá valores reais de URL, tokens ou senhas no repositório. O manifesto de dependências deverá permanecer mínimo e incluir apenas dependências efetivamente usadas.

Alternativa considerada: cada página realizar suas próprias chamadas HTTP. Um cliente compartilhado é preferido para centralizar tratamento de erros e configuração, evitando duplicação entre as páginas.

### Habilitar chamadas somente após confirmar o ambiente

As operações que os arquivos Xano declaram incluem:

- Pacientes: `GET/POST /pacientes` e `GET/PATCH/DELETE /paciente/{paciente_id}`.
- Profissionais: `GET/POST /profissionais` e `GET/PATCH/DELETE /profissional/{profissional_id}`.

Esses caminhos são as rotas declaradas nos arquivos locais, não uma URL base completa nem confirmação de disponibilidade no ambiente implantado. Antes de integrar chamadas, confirmar URL base, requisitos de autenticação e formatos de resposta do ambiente alvo. Até então, não inventar rotas nem simular respostas de sucesso.

### Limitar a primeira entrega à estrutura e navegação

A primeira entrega terá a página Início e as páginas Pacientes e Profissionais navegáveis, sem carregamento de dados ou chamadas HTTP. Essa opção permite validar a estrutura e o fluxo de navegação sem pressupor URL, autenticação ou comportamento da API; as chamadas serão planejadas após resolver as pendências de ambiente.

### Atualizar apenas documentação de arquitetura pertinente

Atualizar `AGENTS.md` e `docs/project-overview.md` para registrar Python/Streamlit como interface e Xano HTTP como backend. O `openspec/config.yaml` já descreve essa arquitetura e o `docs/domain-model.md` permanece independente da escolha de framework; ambos serão preservados.

## Risks / Trade-offs

- [URL base e autenticação ainda não confirmadas] -> Concluir a navegação e a estrutura sem credenciais; bloquear a ativação da integração até confirmar os parâmetros com o responsável pelo ambiente Xano.
- [Valor com aparência sensível encontrado em `xano/api/autentication/autentication.xs`] -> Não copiá-lo para o frontend nem reproduzi-lo em documentação; confirmar se é credencial ativa e, se aplicável, encaminhar remoção segura e rotação antes de uso. Esta Change não altera arquivos Xano.
- [Integração adiada pode demandar uma change posterior] -> Manter esta entrega limitada à navegação; especificar chamadas de leitura ou escrita após aprovação e confirmação dos requisitos do ambiente.

## Migration Plan

Não há migração de dados ou alteração do backend. A implementação futura criará a aplicação em `frontend/`, atualizará a documentação aprovada e executará verificações locais. A reversão consiste em remover os arquivos novos do frontend e reverter somente as alterações documentais dessa Change; os arquivos de `xano/` e as especificações consolidadas permanecem intocados.

## Open Questions

- Qual é a URL base não sensível apropriada para o ambiente de desenvolvimento e como ela será fornecida localmente?
- As APIs alvo exigem autenticação? Se sim, qual fluxo oficialmente configurado deve ser usado pelo frontend?
- O valor com aparência sensível no arquivo do grupo de autenticação é ativo ou apenas metadado? Quem pode confirmar e coordenar eventual rotação?
