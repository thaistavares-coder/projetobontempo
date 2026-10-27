## 1. Registrar o comportamento existente

- [ ] 1.1 Conferir os módulos Pacientes, Profissionais e Especialidades com o contrato e verificar cadastros, listagens e vínculos N:N nas páginas locais.
- [ ] 1.2 Conferir o fluxo de consultas com o contrato e verificar status, intervalos, vínculos obrigatórios e prevenção de conflitos nos testes do serviço SQLite.
- [ ] 1.3 Confirmar que a carga de exemplos é explícita, usa dados fictícios e recusa bancos funcionais não vazios sem alterar seus registros.
- [ ] 1.4 Confirmar por inspeção das páginas e configuração que autenticação, prontuários, disponibilidade profissional e integração ativa com Xano estão fora do MVP local.

## 2. Validar a documentação da Change

- [ ] 2.1 Revisar proposta, especificação e design em conjunto e confirmar que descrevem somente o comportamento implementado.
- [ ] 2.2 Validar a Change com `openspec validate implementar-mvp-local-sqlite --strict --no-interactive` e corrigir apenas inconsistências dos artefatos OpenSpec.
- [ ] 2.3 Executar os testes do frontend e confirmar que o banco SQLite da demonstração é ignorado pelo Git e que os arquivos candidatos não contêm credenciais.
