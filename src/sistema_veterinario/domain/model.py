from dataclasses import dataclass
from datetime import datetime
from datetime import time
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CPF:
    numero: str

    def __post_init__(self):

        if len(self.numero) != 11 or not self.numero.isdigit():
            raise ValueError(
                f"CPF inválido: Deve conter exatamente 11 dígitos. "
                f"Recebido: {self.numero}"
            )

        if self.numero == self.numero[0] * 11:
            raise ValueError(
                "CPF inválido: Não pode conter todos os dígitos iguais."
            )

        for i in (9, 10):
            soma = sum(
                int(self.numero[j]) * (i + 1 - j)
                for j in range(i)
            )
            
            digito = (soma * 10) % 11 % 10

            if int(self.numero[i]) != digito:
                raise ValueError(
                    f"CPF inválido: Dígito verificador na posição {i} incorreto."
                )
                
@dataclass(frozen=True)
class Email:
    endereco: str

    def __post_init__(self) -> None:

        if not self.endereco or not self.endereco.strip():
            raise ValueError("E-mail não pode ser vazio")

        if " " in self.endereco:
            raise ValueError("E-mail não pode conter espaços")

        if self.endereco.count("@") != 1:
            raise ValueError("E-mail deve conter exatamente um '@'")

        local, dominio = self.endereco.split("@")

        if not local:
            raise ValueError("E-mail inválido: parte local (antes do @) vazia")

        if not dominio:
            raise ValueError("E-mail inválido: domínio (depois do @) vazio")

        if "." not in dominio:
            raise ValueError("Domínio do e-mail inválido: falta o ponto (ex: .com)")
            
        if dominio.startswith(".") or dominio.endswith("."):
            raise ValueError("Domínio do e-mail inválido: não pode começar ou terminar com ponto")

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