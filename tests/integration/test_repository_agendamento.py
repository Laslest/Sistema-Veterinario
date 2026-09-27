from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sistema_veterinario.adapters.orm import metadata
from sistema_veterinario.adapters.repository import SqlAlchemyAgendamentoRepository
from sistema_veterinario.domain.model import Agendamento


def test_repository_salva_e_busca_agendamento():
    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)


    Session = sessionmaker(bind=engine)
    session = Session()

    data_futura = datetime.now() + timedelta(days=1)

    agendamento = Agendamento(
        id_agendamento=1,
        id_paciente=20,
        id_veterinario=30,
        id_unidade=40,
        id_tipo_agendamento=50,
        data_hora=data_futura,
    )

    repository = SqlAlchemyAgendamentoRepository(session)

    repository.add(agendamento)
    session.commit()

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_agendamento == 1
    assert resultado.id_paciente == 20
    assert resultado.id_veterinario == 30
    assert resultado.id_unidade == 40
    assert resultado.id_tipo_agendamento == 50
    assert resultado.data_hora == data_futura
    assert resultado.status == "AGENDADO"

    session.close()