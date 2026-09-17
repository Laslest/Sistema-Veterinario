import pytest
from sistema_veterinario.domain.model import Veterinario, Disponibilidade
from datetime import time

def test_adicionar_disponibilidade_conflitante():
    vet = Veterinario(1, "Dr. João", "12345")
    disponibilidade1 = Disponibilidade(inicio=time(9, 0), fim=time(12, 0))
    disponibilidade2 = Disponibilidade(inicio=time(11, 0), fim=time(13, 0))

    vet.adicionar_disponibilidade(disponibilidade1)

    with pytest.raises(ValueError, match="Disponibilidade conflitante."):
        vet.adicionar_disponibilidade(disponibilidade2)

def test_adicionar_disponibilidade_valida():
    vet = Veterinario(1, "Dr. João", "12345")
    disponibilidade1 = Disponibilidade(inicio=time(9, 0), fim=time(12, 0))
    disponibilidade2 = Disponibilidade(inicio=time(12, 0), fim=time(15, 0))
    vet.adicionar_disponibilidade(disponibilidade1)
    vet.adicionar_disponibilidade(disponibilidade2)
    assert len(vet.disponibilidades) == 2
    assert vet.disponibilidades[0] == disponibilidade1
    assert vet.disponibilidades[1] == disponibilidade2

def test_adicionar_disponibilidade_contida(): 
    vet = Veterinario(1, "Dr. João", "12345")
    disponibilidade1 = Disponibilidade(inicio=time(9, 0), fim=time(12, 0))
    disponibilidade2 = Disponibilidade(inicio=time(10, 0), fim=time(11, 0))

    vet.adicionar_disponibilidade(disponibilidade1)

    with pytest.raises(ValueError, match="Disponibilidade conflitante."):
        vet.adicionar_disponibilidade(disponibilidade2)

        