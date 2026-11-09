from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Optional, List
from enum import Enum

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
        
class PoliticaAtendimento(ABC):
    """Define a política de validação do endereço de uma unidade."""

    @abstractmethod
    def validar_endereco(self, endereco: Optional[Endereco]) -> None:
        raise NotImplementedError


class AtendimentoPresencial(PoliticaAtendimento):
    """Política para unidades que realizam atendimento presencial."""

    def validar_endereco(self, endereco: Optional[Endereco]) -> None:
        if endereco is None:
            raise ValueError(
                "Unidade física precisa de um endereço"
            )


class AtendimentoDomiciliar(PoliticaAtendimento):
    """Política para unidades que realizam atendimento domiciliar."""

    def validar_endereco(self, endereco: Optional[Endereco]) -> None:
        return None

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

        # Delega a validação do endereço à política de atendimento
        self.politica_atendimento.validar_endereco(self.endereco)

    @property
    def politica_atendimento(self) -> PoliticaAtendimento:
        if self.atende_domicilio:
            return AtendimentoDomiciliar()

        return AtendimentoPresencial()

    def __eq__(self, outra):
        if not isinstance(outra, Unidade):
            return False

        return self.id_unidade == outra.id_unidade

    def __hash__(self):
        return hash(self.id_unidade)   
      
class DiaSemana(Enum):
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"
    SABADO = "sabado"
    DOMINGO = "domingo"

@dataclass
class Disponibilidade:
    id_disponibilidade: int
    hora_inicio: time
    hora_fim: time
    dia_semana: DiaSemana

    def __post_init__(self):
        if not isinstance(self.dia_semana, DiaSemana):
            raise ValueError(
                "O dia da semana deve ser um valor de DiaSemana"
            )

        if self.hora_inicio >= self.hora_fim:
            raise ValueError(
                "O horário de início deve ser menor do que o horário final"
            )

    def conflita_com(self, outra: "Disponibilidade") -> bool:
        """Verifica se dois intervalos se sobrepoem no mesmo dia."""
        return (
            self.dia_semana == outra.dia_semana
            and self.hora_inicio < outra.hora_fim
            and self.hora_fim > outra.hora_inicio
        )


class IteradorDisponibilidades:
    def __init__(self, disponibilidades, dia_semana=None):
        if dia_semana is not None and not isinstance(dia_semana, DiaSemana):
            raise ValueError("O dia da semana deve ser um valor de DiaSemana")

        self._disponibilidades = list(disponibilidades)
        self._dia_semana = dia_semana
        self._indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self._indice < len(self._disponibilidades):
            atual = self._disponibilidades[self._indice]
            self._indice += 1

            if self._dia_semana is None or atual.dia_semana == self._dia_semana:
                return atual

        raise StopIteration


class Veterinario:
    def __init__(
        self,
        id_veterinario,
        email,
        senha_hash,
        nome,
        crmv,
        especialidade,
    ):
        self.id_veterinario = id_veterinario
        self.email = email
        self.senha_hash = senha_hash
        self.nome = nome
        self.crmv = crmv
        self.especialidade = especialidade
        self.disponibilidades = []

        if (
            not self.email
            or not self.senha_hash
            or not self.nome
            or not self.crmv
            or not self.especialidade
        ):
            raise ValueError("Todos os campos são obrigatórios.")

    
    def iterar_disponibilidades(self, dia_semana=None):
        return IteradorDisponibilidades(self.disponibilidades, dia_semana)

    def adicionar_disponibilidade(self, disponibilidade):
        for existente in self.iterar_disponibilidades(disponibilidade.dia_semana):
            if disponibilidade.conflita_com(existente):
                raise ValueError("Disponibilidade conflitante.")

        self.disponibilidades.append(disponibilidade)


class Relogio(ABC):

    @abstractmethod
    def agora(self) -> datetime:
        raise NotImplementedError


class RelogioDoSistema(Relogio):

    def agora(self) -> datetime:
        return datetime.now()


class EstadoAgendamento:

    nome = None

    def confirmar(self, agendamento):
        raise ValueError(
            "O agendamento não pode ser confirmado, pois não está no status AGENDADO"
        )

    def cancelar(self, agendamento):
        raise ValueError(
            "O agendamento não pode ser cancelado, pois não está no status AGENDADO"
        )

    def concluir(self, agendamento):
        raise ValueError(
            "O agendamento não pode ser concluído, pois não está no status CONFIRMADO"
        )


class Agendado(EstadoAgendamento):

    nome = "AGENDADO"

    def confirmar(self, agendamento):
        agendamento.status = Confirmado.nome

    def cancelar(self, agendamento):
        agendamento.status = Cancelado.nome


class Confirmado(EstadoAgendamento):

    nome = "CONFIRMADO"

    def concluir(self, agendamento):
        agendamento.status = Concluido.nome


class Cancelado(EstadoAgendamento):

    nome = "CANCELADO"


class Concluido(EstadoAgendamento):

    nome = "CONCLUIDO"


ESTADOS_AGENDAMENTO = {
    estado.nome: estado
    for estado in (Agendado(), Confirmado(), Cancelado(), Concluido())
}


class Agendamento:

    def __init__(
        self,
        id_agendamento,
        id_paciente,
        id_veterinario,
        id_unidade,
        id_tipo_agendamento,
        data_hora,
        relogio: Optional[Relogio] = None,
    ):
        if relogio is None:
            relogio = RelogioDoSistema()

        if data_hora <= relogio.agora():
            raise ValueError("A data do agendamento deve ser futura")

        self.id_agendamento = id_agendamento
        self.id_paciente = id_paciente
        self.id_veterinario = id_veterinario
        self.id_unidade = id_unidade
        self.id_tipo_agendamento = id_tipo_agendamento
        self.data_hora = data_hora
        self.status = Agendado.nome

    @property
    def estado(self) -> EstadoAgendamento:
        return ESTADOS_AGENDAMENTO[self.status]

    def confirmar(self):
        self.estado.confirmar(self)

    def cancelar(self):
        self.estado.cancelar(self)

    def concluir(self):
        self.estado.concluir(self)

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

class PacienteFactory(ABC):
    """Define o contrato para criação de pacientes."""

    @abstractmethod
    def criar_paciente(
        self,
        id_paciente: int,
        nome: str,
        data_nascimento: date,
        raca_id: int
    ) -> Paciente:
        raise NotImplementedError


class PacienteFactoryPadrao(PacienteFactory):
    """Implementação padrão da fábrica de pacientes."""

    def criar_paciente(
        self,
        id_paciente: int,
        nome: str,
        data_nascimento: date,
        raca_id: int
    ) -> Paciente:
        return Paciente(
            id_paciente=id_paciente,
            nome=nome,
            data_nascimento=data_nascimento,
            raca_id=raca_id
        )

@dataclass
class Cliente:

    id_cliente: int
    nome: str 
    cpf: CPF
    telefone: Telefone
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