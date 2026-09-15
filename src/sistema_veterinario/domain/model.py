from dataclasses import dataclass
from datetime import time

@dataclass(frozen=True)
class Disponibilidade:
   inicio: time
   fim: time

   def _post_init_(self):
       if self.inicio >= self.fim:
           raise ValueError("O horário de início deve ser menor do que o horário final")

class Veterinario:
   def _init_(self, id_veterinario, nome, crmv):
       self.id_veterinario = id_veterinario
       self.nome = nome
       self.crmv = crmv

class Agendamento:
    def __init__(self, id_agendamento, id_cliente, id_paciente, id_veterinario, data_hora):
        self.id_agendamento = id_agendamento
        self.id_cliente = id_cliente
        self.id_paciente = id_paciente
        self.id_veterinario = id_veterinario
        self.data_hora = data_hora