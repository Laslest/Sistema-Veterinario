import pytest
from sistema_veterinario.domain.model import Veterinario, Disponibilidade, DiaSemana
from datetime import time

def test_adicionar_disponibilidade_conflitante():
    vet = Veterinario(1, "joao@example.com", "hash123", "Dr. João", "12345", "Veterinário")
    disponibilidade1 = Disponibilidade(id_disponibilidade=1, hora_inicio=time(9, 0), hora_fim=time(12, 0), dia_semana=DiaSemana.SEGUNDA)
    disponibilidade2 = Disponibilidade(id_disponibilidade=2, hora_inicio=time(11, 0), hora_fim=time(13, 0), dia_semana=DiaSemana.SEGUNDA)

    vet.adicionar_disponibilidade(disponibilidade1)

    with pytest.raises(ValueError, match="Disponibilidade conflitante."):
        vet.adicionar_disponibilidade(disponibilidade2)

def test_adicionar_disponibilidade_valida():
    vet = Veterinario(1, "joao@example.com", "hash123", "Dr. João", "12345", "Veterinário")
    disponibilidade1 = Disponibilidade(id_disponibilidade=1, hora_inicio=time(9, 0), hora_fim=time(12, 0), dia_semana=DiaSemana.SEGUNDA)
    disponibilidade2 = Disponibilidade(id_disponibilidade=2, hora_inicio=time(12, 0), hora_fim=time(15, 0), dia_semana=DiaSemana.SEGUNDA)
    vet.adicionar_disponibilidade(disponibilidade1)
    vet.adicionar_disponibilidade(disponibilidade2)
    assert len(vet.disponibilidades) == 2
    assert vet.disponibilidades[0] == disponibilidade1
    assert vet.disponibilidades[1] == disponibilidade2

def test_adicionar_disponibilidade_contida(): 
    vet = Veterinario(1, "joao@example.com", "hash123", "Dr. João", "12345", "Veterinário")
    disponibilidade1 = Disponibilidade(id_disponibilidade=1, hora_inicio=time(9, 0), hora_fim=time(12, 0), dia_semana=DiaSemana.SEGUNDA)
    disponibilidade2 = Disponibilidade(id_disponibilidade=2, hora_inicio=time(10, 0), hora_fim=time(11, 0), dia_semana=DiaSemana.SEGUNDA)

    vet.adicionar_disponibilidade(disponibilidade1)

    with pytest.raises(ValueError, match="Disponibilidade conflitante."):
        vet.adicionar_disponibilidade(disponibilidade2)

def test_adicionar_disponibilidade_diferente_dia():
    vet = Veterinario(1, "joao@example.com", "hash123", "Dr. João", "12345", "Veterinário")
    disponibilidade1 = Disponibilidade(id_disponibilidade=1, hora_inicio=time(9, 0), hora_fim=time(12, 0), dia_semana=DiaSemana.SEGUNDA)
    disponibilidade2 = Disponibilidade(id_disponibilidade=2, hora_inicio=time(10, 0), hora_fim=time(13, 0), dia_semana=DiaSemana.TERCA)

    vet.adicionar_disponibilidade(disponibilidade1)
    vet.adicionar_disponibilidade(disponibilidade2)
    assert len(vet.disponibilidades) == 2
    assert vet.disponibilidades[0] == disponibilidade1
    assert vet.disponibilidades[1] == disponibilidade2

def test_veterinario_campos_obrigatorios():
    with pytest.raises(ValueError, match="Todos os campos são obrigatórios."):
        Veterinario(1, "", "hash123", "Dr. João", "12345", "Veterinário")
    with pytest.raises(ValueError, match="Todos os campos são obrigatórios."):
        Veterinario(1, "joao@example.com", "", "Dr. João", "12345", "Veterinário")
    with pytest.raises(ValueError, match="Todos os campos são obrigatórios."):
        Veterinario(1, "joao@example.com", "hash123", "", "12345", "Veterinário")
    with pytest.raises(ValueError, match="Todos os campos são obrigatórios."):
        Veterinario(1, "joao@example.com", "hash123", "Dr. João", "", "Veterinário")
    with pytest.raises(ValueError, match="Todos os campos são obrigatórios."):
        Veterinario(1, "joao@example.com", "hash123", "Dr. João", "12345", "")