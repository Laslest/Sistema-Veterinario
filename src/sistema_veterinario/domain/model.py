from dataclasses import dataclass
from datetime import datetime
from datetime import time

@dataclass(frozen=True)
class Disponibilidade:
    inicio: time
    fim: time

    def __post_init__(self):
        if self.inicio >= self.fim:
            raise ValueError(
                "O horário de início deve ser menor do que o horário final"
            )

class Veterinario:
    def __init__(self, id_veterinario, nome, crmv):
        self.id_veterinario = id_veterinario
        self.nome = nome
        self.crmv = crmv
        self.disponibilidades = []

    def adicionar_disponibilidade(self, disponibilidade):
        for existente in self.disponibilidades:
           if (disponibilidade.inicio < existente.fim and disponibilidade.fim > existente.inicio):
               raise ValueError("Disponibilidade conflitante.")
        self.disponibilidades.append(disponibilidade)

class Agendamento:
    def __init__(self, id_agendamento, id_cliente, id_paciente, id_veterinario, data_hora):
        if data_hora <= datetime.now():
            raise ValueError("A data do agendamento deve ser futura")

        self.id_agendamento = id_agendamento
        self.id_cliente = id_cliente
        self.id_paciente = id_paciente
        self.id_veterinario = id_veterinario
        self.data_hora = data_hora
        self.status = "AGENDADO"

    def confirmar(self):
        if self.status != "AGENDADO":
            raise ValueError(
                "O agendamento não pode ser confirmado, pois não está no status AGENDADO"
            )
        self.status = "CONFIRMADO"


    def cancelar(self):
        if self.status == "AGENDADO":
            self.status = "CANCELADO"
        else:
            raise ValueError(
                "O agendamento não pode ser cancelado, pois não está no status AGENDADO"
            )
            
    def concluir(self):
        if self.status != "CONFIRMADO":
            raise ValueError(
                "O agendamento não pode ser concluído, pois não está no status CONFIRMADO"
            )
        self.status = "CONCLUIDO"