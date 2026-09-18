from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional, List

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

@dataclass(frozen=True)
class CPF:
    numero: str

    def __post_init__(self):

        if len(self.numero) != 11 or not self.numero.isdigit():
            raise ValueError("CPF inválido: Deve conter exatamente 11 dígitos.")

        if self.numero == self.numero[0] * 11:
            raise ValueError("CPF inválido: Não pode conter todos os dígitos iguais.")

        for i in (9, 10):
            soma = sum(
                int(self.numero[j]) * (i + 1 - j)
                for j in range(i)
            )
            
            digito = (soma * 10) % 11 % 10

            if int(self.numero[i]) != digito:
                raise ValueError("CPF inválido.")
                
@dataclass(frozen=True)
class Telefone:
    numero: str

    def __post_init__(self) -> None:
        
        if not self.numero or not self.numero.strip():
            raise ValueError("Telefone não pode ser vazio")

        if not self.numero.isdigit():
            raise ValueError("Telefone inválido: Deve conter somente números.")

        tamanho = len(self.numero)
        if tamanho not in (10, 11):
            raise ValueError("Telefone inválido: Deve ter 10 (fixo) ou 11 (celular) dígitos.")

        ddd = int(self.numero[:2])
        if ddd < 11 or ddd > 99:
            raise ValueError("Telefone inválido: DDD deve estar entre 11 e 99.")

        if tamanho == 11 and self.numero[2] != '9':
            raise ValueError("Telefone inválido: Celulares com 11 dígitos devem começar com '9'.")

@dataclass
class Especie:
    id_especie: int
    nome: str

    def __post_init__(self):

        if not isinstance(self.id_especie, int) or self.id_especie <= 0:
            raise ValueError("O ID da espécie deve ser um número inteiro maior que zero.")

        if not self.nome or self.nome.strip() == "":
            raise ValueError("O nome da espécie não pode ser vazio.")

    def __eq__(self, outra):
        if not isinstance(outra, Especie):
            return False

        return self.id_especie == outra.id_especie

    def __hash__(self):
        return hash(self.id_especie)

@dataclass
class Raca:
    id_raca: int
    nome: str
    id_especie: int

    def __post_init__(self):
        if not isinstance(self.id_raca, int) or self.id_raca <= 0:
            raise ValueError("O ID da raça deve ser um número inteiro maior que zero.")

        if not self.nome or self.nome.strip() == "":
            raise ValueError("O nome da raça não pode ser vazio.")

        if not isinstance(self.id_especie, int) or self.id_especie <= 0:
            raise ValueError("O ID da espécie deve ser um número inteiro maior que zero.")

    def __eq__(self, outra):
        if not isinstance(outra, Raca):
            return False

        return self.id_raca == outra.id_raca

    def __hash__(self):
        return hash(self.id_raca)

@dataclass
class Paciente:
    id_paciente: int
    nome: str
    data_nascimento: date
    raca_id: int

    def __post_init__(self):

        if not isinstance(self.id_paciente, int) or self.id_paciente <= 0:
            raise ValueError("O ID do paciente deve ser um número inteiro maior que zero.")

        if not self.nome or not self.nome.strip():
            raise ValueError("O nome do paciente não pode ser vazio.")

        if not isinstance(self.data_nascimento, date):
            raise ValueError("A data de nascimento deve ser uma data válida.")

        if self.data_nascimento > date.today():
            raise ValueError("A data de nascimento não pode estar no futuro.")

        if not isinstance(self.raca_id, int) or self.raca_id <= 0:
            raise ValueError("O ID da raça deve ser um número inteiro maior que zero.")

    def __eq__(self, outro):
        if not isinstance(outro, Paciente):
            return False
            
        return self.id_paciente == outro.id_paciente
        
    def __hash__(self):
        return hash(self.id_paciente)

@dataclass
class Cliente:

    id_cliente: int
    nome: str
    cpf: CPF
    telefone: Telefone
    endereco: Endereco
    pacientes: List[Paciente] = field(default_factory=list)

    def __post_init__(self) -> None:
        
        if not isinstance(self.id_cliente, int) or self.id_cliente <= 0:
            raise ValueError("O ID do cliente deve ser um número inteiro maior que zero.")

        if not self.nome or not self.nome.strip():
            raise ValueError("O nome do cliente não pode ser vazio.")

        if not isinstance(self.cpf, CPF):
            raise ValueError("O CPF deve ser uma instância válida de CPF.")

        if not isinstance(self.telefone, Telefone):
            raise ValueError(
                "O telefone deve ser uma instância válida de Telefone.")

        if not isinstance(self.endereco, Endereco):
            raise ValueError(
                "O endereço deve ser uma instância válida de Endereco."
            )

    def adicionar_paciente(self, paciente: Paciente) -> None:
        """Adiciona um paciente à coleção do cliente."""
        if not isinstance(paciente, Paciente):
            raise ValueError("O objeto deve ser uma instância da classe Paciente.")

        if any(p.id_paciente == paciente.id_paciente for p in self.pacientes):
            raise ValueError(
                f"Paciente com ID {paciente.id_paciente} já está cadastrado "
                f"para este cliente."
            )

        self.pacientes.append(paciente)

    def buscar_paciente(self, paciente_id: int) -> Paciente:
        """Busca um paciente na coleção; se não pertencer, lança erro."""
        for paciente in self.pacientes:
            if paciente.id_paciente == paciente_id:
                return paciente

        raise ValueError(f"Paciente com ID {paciente_id} não encontrado.")

    def remover_paciente(self, paciente_id: int) -> None:
        """Remove um paciente; se não pertencer, lança erro."""
        for paciente in self.pacientes:
            if paciente.id_paciente == paciente_id:
                self.pacientes.remove(paciente)
                return

        raise ValueError(
            f"Não foi possível remover: Paciente com ID {paciente_id} "
            f"não encontrado."
        )

    def __eq__(self, outro) -> bool:
        """Dois clientes são iguais quando possuem o mesmo id_cliente."""
        if not isinstance(outro, Cliente):
            return False
        return self.id_cliente == outro.id_cliente

    def __hash__(self) -> int:
        return hash(self.id_cliente)