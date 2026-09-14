# PROPOSTA

## Integrantes

- Davi Gesteira - @Laslest
- David Pereira Ramos - @dramos-cpu
- Cauã Raphael - @cauraphael
- Victor dos Santos - @VictorSantosD

## Domínio escolhido

Sistema de Agendamento de Atendimentos Veterinários.

O sistema será voltado para o gerenciamento de atendimentos veterinários,
tendo o médico veterinário como elemento central.

Os clientes poderão cadastrar seus animais e realizar agendamentos.
Os médicos veterinários poderão consultar sua agenda de atendimentos,
incluindo data, horário e local.

Os atendimentos poderão ocorrer em clínicas veterinárias ou a domicílio.
O sistema deverá considerar a duração dos atendimentos e o tempo necessário
de deslocamento entre atendimentos realizados em locais diferentes.

## Entidades de negócio

- Cliente
- Paciente
- Veterinário
- Agendamento
- Unidade
- Horário
- Tipo de Atendimento
- Espécie
- Raça
- Endereço

## Agregados previstos

### Agendamento

Responsável pelo controle dos atendimentos, horários disponíveis, duração das
consultas e conflitos entre agendamentos.

### Cliente / Paciente

Responsável pelos tutores e pelos animais cadastrados no sistema.

### Veterinário

Responsável pelas informações do médico veterinário, sua disponibilidade,
agenda de atendimentos e locais em que poderá realizar consultas.

### Unidade / Local de Atendimento

Responsável pelas clínicas veterinárias e pelos locais onde os atendimentos
serão realizados, incluindo a possibilidade de atendimento a domicílio.

## Divisão inicial de responsabilidades

| Integrante | Responsabilidade |
|---|---|
| Davi Gesteira | Agendamento |
| David Pereira Ramos | Cliente / Paciente |
| Cauã Raphael | Unidade / Local de Atendimento |
| Victor dos Santos | Veterinário |