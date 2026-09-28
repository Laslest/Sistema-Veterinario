from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sistema_veterinario.adapters.orm import metadata
from sistema_veterinario.adapters.repository import SqlAlchemyUnidadeRepository
from sistema_veterinario.domain.model import Endereco, Unidade


def test_repository_salva_e_busca_unidade():
    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    endereco = Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000",
    )

    unidade = Unidade(
        id_unidade=1,
        nome="Clínica A",
        endereco=endereco,
        atende_domicilio=False,
    )

    repository = SqlAlchemyUnidadeRepository(session)

    repository.add(unidade)
    session.commit()

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.nome == "Clínica A"
    assert resultado.endereco.rua == "Rua A"
    assert resultado.endereco.cep == "24000000"
    assert resultado.atende_domicilio is False

    session.close()