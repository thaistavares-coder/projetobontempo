# Domain Model — Sistema de Gestão de Consultório

## 1. Visão geral do domínio

O sistema tem como objetivo organizar o funcionamento de um consultório, principalmente em relação aos pacientes, profissionais, horários disponíveis e agendamentos.

Os principais conceitos do domínio são:

- Paciente
- Profissional
- Disponibilidade
- Agendamento

Esses conceitos se relacionam para permitir o controle da agenda do consultório e evitar conflitos de atendimento.

---

## 2. Paciente

Representa a pessoa que receberá atendimento no consultório.

### Principais informações

- nome;
- dados de identificação;
- dados de contato;
- informações necessárias para realização do atendimento.

### Responsabilidade

O paciente deve possuir um cadastro no sistema para poder ser relacionado a um agendamento.

### Relacionamentos

- um paciente pode possuir vários agendamentos;
- cada agendamento pertence a um único paciente.

---

## 3. Profissional

Representa a pessoa responsável por realizar os atendimentos no consultório.

### Principais informações

- nome;
- dados de identificação;
- dados de contato;
- especialidade ou área de atuação, quando aplicável;
- dias de atendimento;
- horários disponíveis para atendimento.

### Responsabilidade

O profissional representa quem executará o atendimento agendado.

O sistema deverá permitir organizar os dias e horários em que cada profissional estará disponível.

### Relacionamentos

- um profissional pode possuir vários agendamentos;
- cada agendamento deverá estar relacionado a um único profissional;
- um profissional pode possuir várias disponibilidades de atendimento.

---

## 4. Disponibilidade

Representa os dias e horários em que um profissional poderá realizar atendimentos.

### Principais informações

- profissional relacionado;
- dia ou data de atendimento;
- horário inicial;
- horário final ou horários disponíveis;
- situação da disponibilidade.

### Responsabilidade

A disponibilidade deverá informar quando um determinado profissional poderá receber agendamentos.

Ela deverá ser utilizada para ajudar a impedir que sejam criados agendamentos fora dos dias e horários definidos para o profissional.

### Relacionamentos

- uma disponibilidade pertence a um profissional;
- um profissional pode possuir várias disponibilidades;
- os agendamentos deverão respeitar a disponibilidade do profissional.

---

## 5. Agendamento

Representa a reserva de um horário para atendimento de um paciente por um profissional.

### Principais informações

- paciente;
- profissional;
- data do atendimento;
- horário do atendimento;
- situação do agendamento.

### Responsabilidade

O agendamento relaciona um paciente a um profissional em uma determinada data e horário.

O sistema deverá utilizar esse conceito para organizar a agenda do consultório.

### Relacionamentos

- cada agendamento pertence a um paciente;
- cada agendamento pertence a um profissional;
- um paciente pode possuir vários agendamentos;
- um profissional pode possuir vários agendamentos;
- o agendamento deverá respeitar a disponibilidade do profissional.

---

## 6. Relacionamentos principais

Os principais relacionamentos do domínio podem ser representados da seguinte forma:

Paciente
│
└── possui
    │
    └── Agendamento
        │
        └── realizado por
            │
            └── Profissional
                │
                └── possui
                    │
                    └── Disponibilidade

De forma resumida:

- Paciente possui Agendamentos;
- Profissional possui Agendamentos;
- Profissional possui Disponibilidades;
- Agendamento relaciona Paciente e Profissional;
- Agendamento deverá ocorrer dentro da disponibilidade do Profissional.

---

## 7. Regras estruturais importantes

As principais regras estruturais identificadas inicialmente são:

- todo agendamento deverá estar relacionado a um paciente;
- todo agendamento deverá estar relacionado a um profissional;
- todo agendamento deverá possuir data e horário;
- um profissional poderá possuir vários agendamentos em datas e horários diferentes;
- um paciente poderá possuir vários agendamentos;
- um profissional poderá possuir vários períodos ou horários de disponibilidade;
- o sistema não deverá permitir dois agendamentos para o mesmo profissional no mesmo horário;
- o horário de um agendamento deverá respeitar a disponibilidade cadastrada para o profissional.

---

## 8. Observação sobre implementação

Este documento representa o modelo conceitual do domínio.

Ele não define diretamente a estrutura física do banco de dados, nomes de tabelas, tipos de campos ou comandos de criação.

Esses detalhes deverão ser definidos posteriormente, conforme as mudanças do projeto forem especificadas e implementadas de forma incremental.