
from datetime import time

import pytest

from sistema_veterinario.domain.model import (
    DiaSemana,
    Disponibilidade,
    Veterinario,
)


def criar_veterinario():
    return Veterinario(
        1, "vet@example.com", "hash",
        "Dr. Vet", "12345", "Clínica"
    )


def criar_disponibilidade(identificador, dia, inicio, fim):
    return Disponibilidade(
        identificador, time(inicio), time(fim), dia
    )


def test_iterador_percorre_todas_as_disponibilidades():
    vet = criar_veterinario()
    segunda = criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 11)
    terca = criar_disponibilidade(2, DiaSemana.TERCA, 9, 12)

    vet.adicionar_disponibilidade(segunda)
    vet.adicionar_disponibilidade(terca)

    assert list(vet.iterar_disponibilidades()) == [segunda, terca]


def test_iterador_filtra_por_dia_da_semana():
    vet = criar_veterinario()
    seg_manha = criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 11)
    ter = criar_disponibilidade(2, DiaSemana.TERCA, 10, 12)
    seg_tarde = criar_disponibilidade(3, DiaSemana.SEGUNDA, 13, 15)

    for disponibilidade in (seg_manha, ter, seg_tarde):
        vet.adicionar_disponibilidade(disponibilidade)

    assert list(vet.iterar_disponibilidades(DiaSemana.SEGUNDA)) == [
        seg_manha, seg_tarde
    ]
    assert list(vet.iterar_disponibilidades(DiaSemana.TERCA)) == [ter]


def test_iterador_sem_resultados():
    vet = criar_veterinario()
    vet.adicionar_disponibilidade(
        criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 11)
    )

    assert list(vet.iterar_disponibilidades(DiaSemana.DOMINGO)) == []


def test_iterador_finaliza_com_stop_iteration():
    vet = criar_veterinario()
    disp = criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 11)
    vet.adicionar_disponibilidade(disp)

    iterador = vet.iterar_disponibilidades()

    assert iter(iterador) is iterador
    assert next(iterador) == disp

    with pytest.raises(StopIteration):
        next(iterador)


def test_iteradores_mantem_posicoes_independentes():
    vet = criar_veterinario()
    primeira = criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 11)
    segunda = criar_disponibilidade(2, DiaSemana.SEGUNDA, 13, 15)

    vet.adicionar_disponibilidade(primeira)
    vet.adicionar_disponibilidade(segunda)

    iterador_a = vet.iterar_disponibilidades()
    iterador_b = vet.iterar_disponibilidades()

    assert next(iterador_a) == primeira
    assert next(iterador_a) == segunda
    assert next(iterador_b) == primeira


def test_iterador_guarda_lista_do_momento_da_consulta():
    vet = criar_veterinario()
    primeira = criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 11)
    segunda = criar_disponibilidade(2, DiaSemana.SEGUNDA, 13, 15)

    vet.adicionar_disponibilidade(primeira)
    iterador = vet.iterar_disponibilidades()
    vet.adicionar_disponibilidade(segunda)

    assert list(iterador) == [primeira]
    assert list(vet.iterar_disponibilidades()) == [primeira, segunda]


def test_iterador_rejeita_filtro_invalido():
    with pytest.raises(ValueError, match="dia da semana"):
        criar_veterinario().iterar_disponibilidades("segunda")


def test_rejeita_conflito_usando_iterador():
    vet = criar_veterinario()
    vet.adicionar_disponibilidade(
        criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 12)
    )

    with pytest.raises(ValueError, match="Disponibilidade conflitante"):
        vet.adicionar_disponibilidade(
            criar_disponibilidade(2, DiaSemana.SEGUNDA, 11, 13)
        )

    assert len(vet.disponibilidades) == 1


def test_permite_horarios_consecutivos():
    vet = criar_veterinario()
    vet.adicionar_disponibilidade(
        criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 12)
    )
    vet.adicionar_disponibilidade(
        criar_disponibilidade(2, DiaSemana.SEGUNDA, 12, 15)
    )

    assert len(vet.disponibilidades) == 2


def test_permite_sobreposicao_em_dias_diferentes():
    vet = criar_veterinario()
    vet.adicionar_disponibilidade(
        criar_disponibilidade(1, DiaSemana.SEGUNDA, 9, 12)
    )
    vet.adicionar_disponibilidade(
        criar_disponibilidade(2, DiaSemana.TERCA, 9, 12)
    )

    assert len(vet.disponibilidades) == 2
