from dataclasses import dataclass
from datetime import datetime
from datetime import time
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Endereco:
    rua: str
    numero: str
    bairro: str
    cidade: str
    estado: str
    cep: str

    def __post_init__(self):
        # Verifica se a rua está vazia
        if not self.rua.strip():
            raise ValueError("Rua é obrigatória")

        # Verifica se a cidade está vazia
        if not self.cidade.strip():
            raise ValueError("Cidade é obrigatória")

        # Verifica se o estado está vazio
        if not self.estado.strip():
            raise ValueError("Estado é obrigatório")

        # Verifica se o CEP possui exatamente 8 números
        if len(self.cep) != 8 or not self.cep.isdigit():
            raise ValueError("CEP inválido")


@dataclass
class Unidade:
    id_unidade: int
    nome: str
    endereco: Optional[Endereco]
    atende_domicilio: bool

    def __post_init__(self):
        # Verifica se o nome está vazio
        if not self.nome.strip():
            raise ValueError("Nome da unidade é obrigatório")

        # Unidade física precisa ter endereço
        if not self.atende_domicilio and self.endereco is None:
            raise ValueError(
                "Unidade física precisa de um endereço"
            )

    def __eq__(self, outra):
        if not isinstance(outra, Unidade):
            return False

        return self.id_unidade == outra.id_unidade

    def __hash__(self):
        return hash(self.id_unidade)
        
        
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