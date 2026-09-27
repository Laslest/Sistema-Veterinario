from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from sistema_veterinario.domain.model import Agendamento, Cliente


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