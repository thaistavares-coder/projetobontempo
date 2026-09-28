# AGENTS.md — Sistema de Gestão de Consultório

## 1. Objetivo deste arquivo

Este arquivo define como os agentes de Inteligência Artificial devem atuar durante o desenvolvimento do Sistema de Gestão de Consultório.

O agente deve utilizar este documento como orientação operacional e consultar também os demais documentos de contexto do projeto.

---

## 2. Documentação

Antes de realizar alterações significativas, o agente deverá consultar:

- `docs/project-overview.md`
- `docs/domain-model.md`
- `openspec/config.yaml`, quando disponível
- especificações e mudanças existentes dentro de `openspec/`

O agente não deverá tomar decisões importantes sobre o projeto sem considerar a documentação já existente.

---

## 3. Arquitetura

O agente deverá respeitar as tecnologias e a estrutura definidas para o projeto.

O ambiente principal utiliza:

- Visual Studio Code;
- Git;
- GitHub;
- Xano;
- Xano CLI;
- XanoScript;
- GitHub Copilot;
- Xano Developer MCP;
- OpenSpec.

Não introduzir tecnologias alternativas sem necessidade e sem justificativa.

Mudanças que alterem significativamente a arquitetura deverão ser analisadas antes da implementação.

---

## 4. Código

O agente deverá:

- reutilizar código existente quando apropriado;
- evitar duplicação de lógica;
- manter o código simples e compreensível;
- evitar alterações desnecessárias;
- não modificar funcionalidades que não estejam relacionadas à mudança atual;
- respeitar os padrões já existentes no projeto;
- manter o escopo da implementação alinhado à mudança em desenvolvimento.

---

## 5. Domínio

O agente deverá respeitar o modelo de domínio definido em:

`docs/domain-model.md`

Os principais conceitos atuais do sistema são:

- Paciente;
- Profissional;
- Disponibilidade;
- Agendamento.

Antes de criar novos conceitos ou alterar relacionamentos existentes, o agente deverá verificar se a mudança é coerente com o domínio do projeto.

---

## 6. Regras de negócio

As regras de negócio devem ser implementadas preferencialmente no backend.

Entre as regras iniciais importantes estão:

- um agendamento deve possuir um paciente;
- um agendamento deve possuir um profissional;
- um agendamento deve possuir data e horário;
- o horário do agendamento deve respeitar a disponibilidade do profissional;
- um profissional não deve possuir dois agendamentos no mesmo horário.

Novas regras deverão ser documentadas conforme o projeto evoluir.

---

## 7. Segurança

Regras de segurança, autorização e integridade devem ser tratadas no backend.

O frontend não deverá ser considerado como mecanismo suficiente de segurança.

O agente não deverá expor credenciais, tokens ou informações sensíveis em arquivos versionados.

---

## 8. Desenvolvimento com OpenSpec

Mudanças relevantes deverão utilizar OpenSpec.

O agente deverá seguir o fluxo de desenvolvimento definido para o projeto:

1. compreender o contexto;
2. explorar a mudança;
3. propor;
4. revisar;
5. implementar;
6. verificar;
7. arquivar quando concluída.

O agente não deverá implementar mudanças relevantes diretamente sem planejamento quando o fluxo do OpenSpec for aplicável.

---

## 9. Escopo das mudanças

O agente deverá trabalhar de forma incremental.

Cada mudança deve possuir um objetivo claro e um escopo delimitado.

Evitar:

- tentar implementar o sistema inteiro de uma vez;
- alterar funcionalidades sem relação com a mudança atual;
- aumentar o escopo sem necessidade;
- tomar decisões arquiteturais importantes sem revisão.

Quando surgir uma decisão relevante não prevista, o agente deverá interromper a implementação e solicitar análise antes de continuar.

---

## 10. Testes e verificação

Mudanças funcionais deverão possuir uma forma de verificação.

Antes de considerar uma tarefa concluída, o agente deverá:

- verificar se a implementação corresponde ao objetivo da mudança;
- revisar possíveis erros;
- verificar regras de negócio envolvidas;
- validar o comportamento esperado;
- utilizar ferramentas de validação disponíveis quando apropriado.

Para código XanoScript, o Xano Developer MCP poderá ser utilizado para consulta de documentação e validação.

---

## 11. Git e versionamento

O agente deverá considerar que o projeto é versionado com Git e GitHub.

Antes de mudanças relevantes, é recomendável verificar o estado atual do projeto.

Após alterações, o grupo deverá revisar:

- `git status`
- `git diff`

Os commits deverão representar mudanças coerentes e possuir mensagens claras.

---

## 12. Uso de Inteligência Artificial

A IA deve atuar como assistente de desenvolvimento.

O agente pode:

- analisar o projeto;
- consultar documentação;
- sugerir soluções;
- ajudar na especificação;
- gerar código;
- validar código;
- identificar possíveis problemas.

Entretanto, as decisões do projeto continuam sendo responsabilidade do grupo.

O princípio de trabalho deverá ser:

IA propõe  
Aluno analisa  
Aluno aprova ou corrige  
IA implementa

---

## 13. Fonte de verdade

O agente deverá priorizar:

1. documentação do projeto;
2. especificações OpenSpec;
3. documentação oficial das ferramentas;
4. Xano Developer MCP para informações específicas de XanoScript e Xano CLI.

Não presumir sintaxe ou comportamento de ferramentas quando houver possibilidade de consultar documentação oficial.