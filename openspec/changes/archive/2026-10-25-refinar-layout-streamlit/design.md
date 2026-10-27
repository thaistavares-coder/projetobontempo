## Context

A navegação usa `st.navigation` e já contém as páginas Início, Pacientes e Profissionais. As páginas atuais exibem apenas conteúdo informativo e não fazem chamadas HTTP. As especificações de domínio confirmam os campos exibidos nas tabelas; consulte `proposal.md` e `specs/interface-web/spec.md` para o escopo e os comportamentos requeridos.

## Goals / Non-Goals

**Goals:**

- Refinar a hierarquia visual sem substituir a estrutura multipágina existente.
- Exibir affordances administrativas reconhecíveis, deixando claro que busca e criação ainda não estão disponíveis.
- Manter leitura e navegação confortáveis em larguras típicas de notebook.

**Non-Goals:**

- Conectar os elementos de tela a estado persistente, rotas de API ou formulários de cadastro.
- Alterar o tema global de execução do Streamlit por configuração externa ou adicionar bibliotecas visuais.

## Decisions

- Preservar `st.navigation` e limitar os destinos aos três módulos existentes. Os cards de Pacientes e Profissionais apontam para essas páginas existentes; Agenda é apenas um rótulo informativo, sem ação ou página.
- Construir cabeçalhos e cards com componentes Streamlit e ícones compatíveis com a biblioteca já instalada. Aplicar CSS pontual somente para identidade visual, hierarquia, espaçamento e responsividade; evitar HTML estrutural extenso e frameworks externos.
- Nas páginas de módulos, representar a busca com um campo desabilitado e o botão de criação com estado desabilitado. Isso comunica o formato esperado sem sugerir que a operação funciona ou persiste dados.
- Renderizar a tabela a partir de uma estrutura sem linhas e com colunas previamente definidas. Pacientes usa ID, Nome, Telefone e E-mail; Profissionais usa ID, Nome e Especialidade, alinhados às especificações existentes. Não preencher a tabela com exemplos, placeholders que pareçam registros ou resultados inventados.
- Manter mensagem de integração indisponível visível em cada módulo. A ausência de chamadas ao Xano é estrutural, não apenas uma mensagem apresentada na interface.

## Risks / Trade-offs

- [Controles desabilitados podem parecer pouco interativos] → A mensagem explícita de integração pendente e o estado visual desabilitado comunicam que são apenas elementos de apresentação.
- [CSS customizado pode variar entre versões ou larguras de tela] → Limitar seletores e estilos ao necessário e verificar visualmente as três páginas em viewport de notebook.
- [Uma tabela sem linhas pode parecer incompleta] → Manter cabeçalhos de coluna visíveis e acompanhar a tabela com a mensagem de integração indisponível, sem inventar conteúdo.
