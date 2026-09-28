# Project Overview — Sistema de Gestão de Consultório

## 1. Visão geral

Este projeto acadêmico é desenvolvido para a disciplina de Innovation Labs, ministrada pelo professor Bontempo.

O sistema tem como objetivo realizar o controle de um consultório, organizando informações relacionadas aos pacientes, agendamentos, profissionais responsáveis pelos atendimentos, horários disponíveis e dias de atendimento.

A proposta é centralizar essas informações em um único sistema, facilitando a organização da rotina do consultório e o controle dos atendimentos.

## 2. Problema

Um consultório precisa organizar de forma clara os pacientes, profissionais, dias de atendimento, horários disponíveis e agendamentos.

Quando essas informações não estão centralizadas, podem ocorrer problemas como conflitos de horários, dificuldade para visualizar a disponibilidade dos profissionais e falhas no controle dos atendimentos.

O sistema busca organizar essas informações e facilitar o gerenciamento da agenda do consultório.

## 3. Objetivos

O objetivo principal do projeto é desenvolver um sistema para auxiliar no gerenciamento da agenda e dos atendimentos de um consultório.

Entre os objetivos iniciais estão:

- controlar os pacientes cadastrados;
- controlar os profissionais responsáveis pelos atendimentos;
- registrar os dias de atendimento dos profissionais;
- registrar os horários disponíveis;
- controlar os agendamentos;
- facilitar a visualização da agenda;
- evitar conflitos de horários.

## 4. Público-alvo / usuários

Os principais usuários do sistema serão as pessoas responsáveis pela organização e pelo gerenciamento dos atendimentos do consultório.

O sistema também deverá considerar:

- profissionais responsáveis pelos atendimentos;
- pacientes cadastrados no consultório.

## 5. Escopo

O escopo inicial do projeto contempla o controle das principais informações necessárias para o funcionamento da agenda do consultório.

Inicialmente, o sistema deverá considerar:

- cadastro e controle de pacientes;
- cadastro e controle de profissionais;
- definição dos dias de atendimento dos profissionais;
- definição dos horários disponíveis;
- criação e controle de agendamentos;
- organização da agenda do consultório;
- relacionamento entre paciente, profissional, data e horário do atendimento.

Funcionalidades adicionais poderão ser definidas durante a evolução do projeto.

## 6. Principais funcionalidades

As principais funcionalidades previstas inicialmente são:

- cadastrar pacientes;
- consultar pacientes cadastrados;
- cadastrar profissionais;
- consultar profissionais cadastrados;
- definir dias de atendimento dos profissionais;
- definir horários de atendimento;
- consultar horários disponíveis;
- criar agendamentos;
- consultar agendamentos;
- relacionar cada agendamento a um paciente;
- relacionar cada agendamento a um profissional;
- registrar a data e o horário do atendimento;
- controlar a disponibilidade de horários;
- evitar conflitos de agendamento para um mesmo profissional.

## 7. Requisitos e restrições importantes

O sistema deverá manter a organização e a integridade das informações relacionadas aos atendimentos.

Entre as regras iniciais consideradas importantes estão:

- um agendamento deverá estar relacionado a um paciente;
- um agendamento deverá estar relacionado a um profissional;
- o agendamento deverá possuir data e horário definidos;
- os horários disponíveis deverão respeitar os dias e horários de atendimento dos profissionais;
- um profissional não deverá possuir dois atendimentos agendados para o mesmo horário;
- as regras detalhadas de funcionamento serão definidas de forma incremental durante o desenvolvimento.

## 8. Arquitetura tecnológica

O projeto utilizará o ambiente de desenvolvimento definido para a disciplina.

As principais ferramentas utilizadas serão:

- Visual Studio Code;
- Git;
- GitHub;
- Xano;
- Xano CLI;
- XanoScript;
- GitHub Copilot;
- Xano Developer MCP;
- OpenSpec.

O Xano será utilizado como parte do backend da aplicação e o projeto será versionado utilizando Git e GitHub.

## 9. Princípios de desenvolvimento

O projeto será desenvolvido de forma incremental.

As funcionalidades serão analisadas, especificadas, implementadas e revisadas em etapas menores.

Sempre que possível, as mudanças relevantes deverão ser planejadas antes da implementação.

O desenvolvimento deverá utilizar o OpenSpec para organizar e documentar as mudanças do projeto.

## 10. Segurança e integridade

O sistema deverá preservar a integridade das informações relacionadas a pacientes, profissionais e agendamentos.

As regras relacionadas à disponibilidade de horários e conflitos de agenda deverão ser validadas no backend.

Regras específicas de autenticação, autorização e controle de acesso poderão ser definidas conforme a evolução do projeto.

## 11. Estratégia de desenvolvimento

O desenvolvimento será realizado através de mudanças incrementais.

Antes de implementar funcionalidades relevantes, o grupo deverá analisar o objetivo da mudança, seu impacto e suas regras.

O OpenSpec será utilizado para auxiliar na especificação das mudanças.

O Git e o GitHub serão utilizados para controle de versão, histórico das alterações e organização do desenvolvimento.

## 12. Fonte de verdade e documentação

A documentação do projeto deverá ser mantida nos arquivos de contexto e nas especificações do OpenSpec.

Os documentos principais de contexto deverão representar a visão geral, o domínio e as regras de desenvolvimento do projeto.

As mudanças relevantes deverão ser especificadas, revisadas e registradas antes ou durante sua implementação, de acordo com o fluxo adotado pelo OpenSpec.