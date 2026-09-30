import pytest
from datetime import time

from sistema_veterinario.adapters.repository import FakeVeterinarioRepository
from sistema_veterinario.domain.model import DiaSemana
from sistema_veterinario.service_layer.services import cadastrar_veterinario, buscar_veterinario, adicionar_disponibilidade_veterinario

def test_cadastrar_veterinario():
    repository = FakeVeterinarioRepository()
    
    veterinario = cadastrar_veterinario(
        repository=repository,
        id_veterinario=1,
        email="veterinario@example.com",
        senha_hash="hashed_password",
        nome="Veterinário Exemplo",
        crmv="CRMV-12345",
        especialidade="Especialidade Exemplo"
    )

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado is veterinario
    assert resultado.id_veterinario == 1
    assert resultado.email == "veterinario@example.com"
    assert resultado.senha_hash == "hashed_password"
    assert resultado.nome == "Veterinário Exemplo"
    assert resultado.crmv == "CRMV-12345"
    assert resultado.especialidade == "Especialidade Exemplo"

def test_buscar_veterinario_existente():
    repository = FakeVeterinarioRepository()
    veterinario = cadastrar_veterinario(
        repository=repository,
        id_veterinario=1,
        email="veterinario@example.com",
        senha_hash="hashed_password",
        nome="Veterinário Exemplo",
        crmv="CRMV-12345",
        especialidade="Especialidade Exemplo"
    )

    resultado = buscar_veterinario(repository, 1)

    assert resultado is not None
    assert resultado is veterinario
    assert resultado.id_veterinario == 1
    assert resultado.email == "veterinario@example.com"
    assert resultado.senha_hash == "hashed_password"
    assert resultado.nome == "Veterinário Exemplo"
    assert resultado.crmv == "CRMV-12345"
    assert resultado.especialidade == "Especialidade Exemplo"

def test_buscar_veterinario_inexistente():
    repository = FakeVeterinarioRepository()

    with pytest.raises(ValueError) as excinfo:
        buscar_veterinario(repository, 999)

    assert str(excinfo.value) == "Veterinário não encontrado"

def test_adicionar_disponibilidade_veterinario():
    repository = FakeVeterinarioRepository()
    cadastrar_veterinario(
        repository=repository,
        id_veterinario=1,
        email="veterinario@example.com",
        senha_hash="hashed_password",
        nome="Veterinário Exemplo",
        crmv="CRMV-12345",
        especialidade="Especialidade Exemplo"
    )



    disponibilidade = adicionar_disponibilidade_veterinario(repository, 1, 1, DiaSemana.SEGUNDA, time(9, 0), time(17, 0))

    resultado = repository.get(1)

    assert resultado is not None
    assert len(resultado.disponibilidades) == 1
    assert resultado.disponibilidades[0].id_disponibilidade == 1
    assert resultado.disponibilidades[0].dia_semana == DiaSemana.SEGUNDA
    assert resultado.disponibilidades[0].hora_inicio == time(9, 0)
    assert resultado.disponibilidades[0].hora_fim == time(17, 0)
    assert resultado.disponibilidades[0] is disponibilidade