
from datetime import time

import pytest

from sistema_veterinario.domain.model import (
    DiaSemana,
    Disponibilidade,
    Veterinario,
)


@pytest.mark.parametrize(
    "dia, inicio, fim, esperado",
    [
        (DiaSemana.SEGUNDA, time(11), time(13), True),
        (DiaSemana.SEGUNDA, time(10), time(11), True),
        (DiaSemana.SEGUNDA, time(8), time(10), True),
        (DiaSemana.SEGUNDA, time(12), time(15), False),
        (DiaSemana.SEGUNDA, time(7), time(9), False),
        (DiaSemana.TERCA, time(10), time(11), False),
        (DiaSemana.SEGUNDA, time(9), time(12), True),
    ],
)
def test_conflita_com(dia, inicio, fim, esperado):
    original = Disponibilidade(
        id_disponibilidade=1,
        hora_inicio=time(9),
        hora_fim=time(12),
        dia_semana=DiaSemana.SEGUNDA,
    )

    outra = Disponibilidade(
        id_disponibilidade=2,
        hora_inicio=inicio,
        hora_fim=fim,
        dia_semana=dia,
    )

    assert original.conflita_com(outra) is esperado
    assert outra.conflita_com(original) is esperado


def test_veterinario_mantem_erro_em_conflito():
    veterinario = Veterinario(
        1,
        "vet@example.com",
        "hash",
        "Vet",
        "123",
        "Clinica",
    )

    original = Disponibilidade(
        1, time(9), time(12), DiaSemana.SEGUNDA
    )

    conflitante = Disponibilidade(
        2, time(11), time(13), DiaSemana.SEGUNDA
    )

    veterinario.adicionar_disponibilidade(original)

    with pytest.raises(
        ValueError, match=r"Disponibilidade conflitante\."
    ):
        veterinario.adicionar_disponibilidade(conflitante)

    assert veterinario.disponibilidades == [original]


def test_veterinario_permite_horarios_consecutivos():
    veterinario = Veterinario(
        1,
        "vet@example.com",
        "hash",
        "Vet",
        "123",
        "Clinica",
    )

    primeira = Disponibilidade(
        1, time(9), time(12), DiaSemana.SEGUNDA
    )

    segunda = Disponibilidade(
        2, time(12), time(15), DiaSemana.SEGUNDA
    )

    veterinario.adicionar_disponibilidade(primeira)
    veterinario.adicionar_disponibilidade(segunda)

    assert veterinario.disponibilidades == [
        primeira,
        segunda,
    ]
