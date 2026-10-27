## 1. Pré-condições e inventário do Xano

- [ ] 1.1 No ambiente Xano de destino autorizado, comparar tabelas, índices, FKs, APIs, dados e permissões com os arquivos versionados; registrar separadamente fatos locais e remotos, sem executar gravações nem usar dados reais.
- [ ] 1.2 Confirmar na documentação e no ambiente de desenvolvimento a sintaxe/suporte para tipos `int`, `text`, `bool` e `timestamp`, FKs, unicidade composta, unicidade de campo normalizado e garantias atômicas; confirmar a política de fuso proposta `America/Sao_Paulo` e produzir evidência reproduzível antes de qualquer alteração física.
- [ ] 1.3 Confirmar backup, rollback e uso exclusivo de dados fictícios; obter destino não-live autorizado, isolar os quatro novos arquivos e revisar um novo `--dry-run` sem atualizações de recursos existentes nem referências não resolvidas. Manter publicação e integração bloqueadas enquanto a única branch visível for live (`v1`) ou os controles de acesso sem login não estiverem verificados e aprovados.

## 2. Esquema aditivo e integridade referencial

- [ ] 2.1 Criar `especialidade` com chave primária inteira e `nome` mais chave normalizada pelo backend; verificar que trim/caixa geram unicidade, acentos são preservados e nomes duplicados são rejeitados.
- [ ] 2.2 Criar `profissional_especialidade` com FKs obrigatórias para profissional e especialidade e unicidade do par; verificar rejeição de referências inexistentes e duplicidade, aceitando pares distintos.
- [ ] 2.3 Criar `status_consulta` com código único, nome e indicador de ocupação; semear somente os cinco valores aprovados (`agendada`, `confirmada`, `realizada`, `cancelada`, `nao_compareceu`) e verificar a ocupação definida no design, sem criar histórico de transições.
- [ ] 2.4 Criar `consulta` com FKs obrigatórias para paciente, profissional, especialidade e status e campos `inicio_em` e `fim_em` do tipo timestamp; verificar rejeição de referências ausentes/inexistentes, de intervalo fora do mesmo dia local e de `fim_em` não posterior a `inicio_em`.
- [ ] 2.5 Aplicar política sem cascata destrutiva e índices necessários; verificar unicidade, integridade referencial e preservação das tabelas, IDs, registros e endpoints preexistentes em ambiente isolado antes de promover qualquer alteração.

## 3. Regras de associação e agenda no backend

- [ ] 3.1 Implementar associação de médico a especialidades sem mínimo obrigatório durante a transição; verificar que uma consulta só aceita a especialidade efetivamente associada ao profissional selecionado.
- [ ] 3.2 Implementar gravação de consulta com todas as referências e dados obrigatórios de forma atômica; testar entradas inválidas e confirmar ausência de persistência parcial.
- [ ] 3.3 Impedir intervalos timestamp sobrepostos no mesmo dia local para o mesmo médico quando ambas as consultas estão com status que ocupa horário; verificar intervalos adjacentes permitidos, médicos diferentes independentes e criação concorrente protegida.
- [ ] 3.4 Manter apenas o status atual na tabela de consulta e restringir exclusões de referências em uso; implementar transições de status somente após aprovação da política em Change de APIs/regras própria e verificar os cenários aprovados.

## 4. Compatibilidade e migração segura

- [ ] 4.1 Manter `profissional.especialidade` e os contratos existentes de Pacientes e Profissionais sem alterações; verificar que nenhuma tabela associativa é preenchida automaticamente a partir do texto legado.
- [ ] 4.2 Planejar eventual reconciliação do texto legado em Change separada, com mapeamento revisável, tratamento de não correspondências, cópia de segurança, contagens antes/depois e rollback; verificar que nenhum dado é sobrescrito.
- [ ] 4.3 Executar testes de esquema e regras somente com dados sintéticos, incluindo FKs inválidas, duplicidade, especialidade incompatível e conflitos; verificar que nenhum teste consulta endpoints públicos ou inclui dados pessoais/clínicos reais.

## 5. Revisão e liberação

- [ ] 5.1 Revisar o diff XanoScript e a validação disponível no Xano Developer MCP; verificar que os arquivos versionados correspondem às decisões aprovadas e não declaram o estado publicado sem evidência.
- [ ] 5.2 Antes de disponibilizar qualquer API ou integrar o Streamlit, aprovar e verificar os controles de acesso, retenção e exposição compatíveis com a ausência de login; confirmar operação local exclusivamente com dados fictícios e obter autorização explícita para habilitação.
