from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sistema_veterinario.adapters.orm import metadata
from sistema_veterinario.adapters.repository import SqlAlchemyVeterinarioRepository
from sistema_veterinario.domain.model import Veterinario, Disponibilidade, DiaSemana



def test_repository_salva_e_busca_veterinario():
    engine = create_engine("sqlite:///:memory:")

    metadata.create_all(engine)


    Session = sessionmaker(bind=engine)
    session = Session()

    disponibilidade1 = Disponibilidade(
        id_disponibilidade=1, 
        hora_inicio=time(9, 0), 
        hora_fim=time(12, 0), 
        dia_semana=DiaSemana.SEGUNDA)

    
    veterinario = Veterinario(
        id_veterinario=1,
        email="carlos@example.com",
        senha_hash="hash123",
        nome="Dr. Carlos",
        crmv="12345",
        especialidade="Neurologista"
    )

    veterinario.adicionar_disponibilidade(disponibilidade1)

    repository = SqlAlchemyVeterinarioRepository(session)

    repository.add(veterinario)
    session.commit()
    session.expunge_all()

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_veterinario == 1
    assert resultado.email == "carlos@example.com"
    assert resultado.senha_hash == "hash123"
    assert resultado.nome == "Dr. Carlos"
    assert resultado.crmv == "12345"
    assert resultado.especialidade == "Neurologista"
    assert len(resultado.disponibilidades) == 1
    assert resultado.disponibilidades[0].id_disponibilidade == 1
    assert resultado.disponibilidades[0].hora_inicio == time(9, 0)
    assert resultado.disponibilidades[0].hora_fim == time(12, 0)
    assert resultado.disponibilidades[0].dia_semana == DiaSemana.SEGUNDA
    session.close()
