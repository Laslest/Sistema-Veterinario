from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sistema_veterinario.adapters.orm import metadata
from sistema_veterinario.adapters.repository import SqlAlchemyClienteRepository
from sistema_veterinario.domain.model import Cliente, CPF, Paciente, Telefone


def test_repository_salva_e_busca_cliente():
    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    cliente = Cliente(
        id_cliente=1,
        nome="João Silva",
        cpf=CPF(numero="52998224725"),
        telefone=Telefone(numero="11999999999"),
    )

    repository = SqlAlchemyClienteRepository(session)

    repository.add(cliente)
    session.commit()
    session.expunge_all()

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_cliente == 1
    assert resultado.nome == "João Silva"
    assert isinstance(resultado.cpf, CPF)
    assert resultado.cpf.numero == "52998224725"
    assert isinstance(resultado.telefone, Telefone)
    assert resultado.telefone.numero == "11999999999"

    session.close()


def test_repository_salva_cliente_com_paciente():
    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    cliente = Cliente(
        id_cliente=1,
        nome="João Silva",
        cpf=CPF(numero="52998224725"),
        telefone=Telefone(numero="11999999999"),
    )

    paciente = Paciente(
        id_paciente=10,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=5,
    )

    cliente.adicionar_paciente(paciente)

    repository = SqlAlchemyClienteRepository(session)

    repository.add(cliente)
    session.commit()
    session.expunge_all()

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_cliente == 1
    assert len(resultado.pacientes) == 1

    paciente_recuperado = resultado.pacientes[0]
    assert paciente_recuperado.id_paciente == 10
    assert paciente_recuperado.nome == "Rex"
    assert paciente_recuperado.data_nascimento == date(2020, 5, 10)
    assert paciente_recuperado.raca_id == 5

    session.close()


def test_repository_busca_cliente_inexistente_retorna_none():
    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    repository = SqlAlchemyClienteRepository(session)

    resultado = repository.get(999)

    assert resultado is None

    session.close()