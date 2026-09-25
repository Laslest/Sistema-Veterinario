from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from sistema_veterinario.domain.model import Agendamento


class AbstractRepository(ABC):

    @abstractmethod
    def add(self, agendamento: Agendamento):
        raise NotImplementedError

    @abstractmethod
    def get(self, id_agendamento: int):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, agendamento: Agendamento):
        self.session.add(agendamento)

    def get(self, id_agendamento: int):
        return self.session.get(Agendamento, id_agendamento)