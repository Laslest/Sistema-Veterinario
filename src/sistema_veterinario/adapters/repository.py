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

class ClienteJaCadastradoError(Exception):
    """Erro lançado quando um cliente com o mesmo ID já existe."""
    pass

class ClienteRepository(AbstractRepository):
    """
    Contrato do repositório do agregado Cliente/Paciente.

    Um cliente existente não pode ser substituído por outro
    com o mesmo identificador.
    """

    @abstractmethod
    def add(self, cliente: Cliente):
        raise NotImplementedError

class SqlAlchemyAgendamentoRepository(AbstractRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, agendamento: Agendamento):
        self.session.add(agendamento)

    def get(self, id_agendamento: int):
        return self.session.get(Agendamento, id_agendamento)


class SqlAlchemyClienteRepository(ClienteRepository):

    def __init__(self, session: Session):
        self.session = session

    def add(self, cliente: Cliente):
        outro_pendente = any(
            isinstance(entidade, Cliente)
            and entidade.id_cliente == cliente.id_cliente
            and entidade is not cliente
            for entidade in self.session.new
        )

        if outro_pendente:
            raise ClienteJaCadastradoError(
                f"Cliente com ID {cliente.id_cliente} já cadastrado"
            )

        with self.session.no_autoflush:
            existente = self.session.get(Cliente, cliente.id_cliente)

        if existente is not None and existente is not cliente:
            raise ClienteJaCadastradoError(
                f"Cliente com ID {cliente.id_cliente} já cadastrado"
            )

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


class FakeClienteRepository(ClienteRepository):

    def __init__(self):
        self.clientes = {}

    def add(self, cliente: Cliente):
        existente = self.clientes.get(cliente.id_cliente)

        if existente is not None and existente is not cliente:
            raise ClienteJaCadastradoError(
                f"Cliente com ID {cliente.id_cliente} já cadastrado"
            )
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