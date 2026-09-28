from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from sistema_veterinario.domain.model import Agendamento, Cliente, Veterinario, Unidade


class AbstractRepository(ABC):

    @abstractmethod
    def add(self, entidade):
        raise NotImplementedError

    @abstractmethod
    def get(self, id_entidade):
        raise NotImplementedError


class SqlAlchemyAgendamentoRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, agendamento: Agendamento):
        self.session.add(agendamento)

    def get(self, id_agendamento: int):
        return self.session.get(Agendamento, id_agendamento)


class SqlAlchemyClienteRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, cliente: Cliente):
        self.session.add(cliente)

    def get(self, id_cliente: int):
        return self.session.get(Cliente, id_cliente)


class SqlAlchemyVeterinarioRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, veterinario: Veterinario):
        self.session.add(veterinario)

    def get(self, id_veterinario: int):
        return self.session.get(Veterinario, id_veterinario)

class SqlAlchemyUnidadeRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, unidade: Unidade):
        self.session.add(unidade)

    def get(self, id_unidade: int):
        return self.session.get(Unidade, id_unidade)   


class FakeAgendamentoRepository(AbstractRepository):

    def __init__(self):
        self.agendamentos = {}

    def add(self, agendamento: Agendamento):
        self.agendamentos[agendamento.id_agendamento] = agendamento

    def get(self, id_agendamento: int):
        return self.agendamentos.get(id_agendamento)


class FakeVeterinarioRepository(AbstractRepository):

    def __init__(self):
        self.veterinarios = {}

    def add(self, veterinario: Veterinario):
        self.veterinarios[veterinario.id_veterinario] = veterinario

    def get(self, id_veterinario: int):
        return self.veterinarios.get(id_veterinario)


class FakeClienteRepository(AbstractRepository):

    def __init__(self):
        self.clientes = {}

    def add(self, cliente: Cliente):
        self.clientes[cliente.id_cliente] = cliente

    def get(self, id_cliente: int):
        return self.clientes.get(id_cliente)

class FakeUnidadeRepository(AbstractRepository):

    def __init__(self):
        self.unidades = {}

    def add(self, unidade: Unidade):
        self.unidades[unidade.id_unidade] = unidade

    def get(self, id_unidade: int):
        return self.unidades.get(id_unidade)    