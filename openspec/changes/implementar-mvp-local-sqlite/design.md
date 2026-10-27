## Context

Consulte [proposal.md](./proposal.md) para a motivação e [specs/mvp-local-sqlite/spec.md](./specs/mvp-local-sqlite/spec.md) para o contrato observável. A implementação existente usa Streamlit para as páginas e SQLite com chaves estrangeiras para persistência; o caminho padrão do banco está em `frontend/data/bontempo_demo.sqlite3`. O README inicia o servidor no endereço de loopback `127.0.0.1:8502`.

O projeto também contém um cliente GET para listagens do Xano, mas as páginas deste modo local chamam o serviço SQLite e não usam esse cliente. A configuração e os endpoints existentes do Xano permanecem fora desta Change. O MVP local diverge da arquitetura-alvo descrita na documentação geral e deve ser entendido como uma demonstração independente, não como integração ou substituto do backend Xano.

## Goals / Non-Goals

**Goals:**

- Registrar com precisão a composição e o comportamento local já implementados.
- Preservar o isolamento da demonstração e explicitar as limitações relevantes antes do uso em apresentação.
- Manter a Change restrita a documentação OpenSpec e verificações, sem modificar código funcional, Xano ou endpoints.

**Non-Goals:**

- Implementar ou aplicar funcionalidades; esta Change documenta retrospectivamente o MVP já existente.
- Habilitar chamadas Xano, sincronização de dados, autenticação ou publicação em rede.
- Introduzir prontuários, disponibilidade, edição/exclusão de registros ou uso com dados reais.

## Decisions

### Manter SQLite como armazenamento exclusivo do modo de demonstração

As páginas locais usam o serviço SQLite e o arquivo padrão no diretório `frontend/data`. O arquivo do banco é ignorado pelo Git. A alternativa de apontar as páginas para o cliente HTTP existente foi rejeitada para esta demonstração: esse cliente é uma integração GET separada, permanece desabilitado por padrão e não é consumido pelas telas do MVP.

### Representar especialidades em associação N:N e consultas com intervalos

O modelo local relaciona profissionais e especialidades por uma tabela de associação e vincula cada consulta a paciente, profissional, especialidade e status. A escolha corresponde aos comportamentos observáveis nas telas e serviços atuais; não altera o modelo ou os endpoints do Xano.

### Validar conflitos por sobreposição e status

O serviço impede sobreposição entre consultas do mesmo profissional que ocupam horário. Agendada e Confirmada ocupam o horário; Realizada, Cancelada e Não compareceu não ocupam. Intervalos adjacentes são aceitos. Não existe verificação de disponibilidade profissional, portanto a validação de conflito não equivale a confirmar que o profissional trabalha naquele dia ou horário.

### Usar exemplos sintéticos somente por ação explícita

A carga inicial de demonstração é acionada pela interface e recusa bancos com dados funcionais, preservando o conteúdo existente. Os registros são fictícios; a ação não é uma migração nem um reset do banco.

### Separar revisão de contraste do agrupamento da implementação

As alterações atuais de `frontend/ui.py` tratam dos estilos CSS de contraste, foco e botões, junto com os helpers visuais usados pelas páginas. Essa mistura torna o staging parcial do arquivo arriscado. Para commits funcionais e de CSS, recomenda-se consolidar as duas mudanças ou preparar uma separação revisada manualmente; não realizar staging parcial automático.

## Risks / Trade-offs

- [Sem autenticação ou autorização] → O MVP é apenas demonstração local e não deve ser exposto à rede nem receber dados pessoais ou clínicos reais.
- [Sem disponibilidade profissional] → A prevenção de conflito só compara consultas existentes do profissional; ela não prova que um horário está dentro de uma jornada de atendimento.
- [Sem integração ativa com Xano] → Dados locais não são enviados nem sincronizados; mudanças no banco SQLite não alteram o backend.
- [SQLite em arquivo local] → O banco pertence ao computador e ao ambiente da demonstração; não há coordenação multiusuário nem garantia de backup ou sincronização.
- [Staging da estilização] → `frontend/ui.py` contém CSS junto a helpers visuais e não oferece uma divisão de commit confiável por arquivo sem staging parcial cuidadoso.

## Migration Plan

Não há migração nem implantação nesta Change. A aplicação continua iniciada pelo comando local do README; o arquivo SQLite permanece local e ignorado pelo Git. Nenhum passo de rollback de banco, alteração de endpoint, archive, deploy ou publicação é realizado.

## Open Questions

Não há decisões pendentes para registrar a implementação atual. Autenticação, prontuários, disponibilidade profissional e integração Xano dependem de Changes futuras e aprovação próprias.
