from datetime import time
import pytest
from sistema_veterinario.domain.model import Disponibilidade, DiaSemana

def test_disponibilidade_valida():
    id_disponibilidade = 1
    hora_inicio = time(9, 0)
    hora_fim = time(12, 0)
    dia_semana = DiaSemana.SEGUNDA
    disponibilidade = Disponibilidade(id_disponibilidade=id_disponibilidade, hora_inicio=hora_inicio, hora_fim=hora_fim, dia_semana=dia_semana)
    assert disponibilidade.hora_inicio == hora_inicio
    assert disponibilidade.hora_fim == hora_fim
    assert disponibilidade.dia_semana == dia_semana
    assert disponibilidade.id_disponibilidade == id_disponibilidade

def test_disponibilidade_invalida():
    id_disponibilidade = 2
    hora_inicio = time(14, 0)
    hora_fim = time(12, 0)
    dia_semana = DiaSemana.SEGUNDA
    with pytest.raises(ValueError, match="O horário de início deve ser menor do que o horário final"):
        Disponibilidade(id_disponibilidade=id_disponibilidade, hora_inicio=hora_inicio, hora_fim=hora_fim, dia_semana=dia_semana)

def test_disponibilidade_inicio_igual_fim():
    id_disponibilidade = 3
    hora_inicio = time(10, 0)
    hora_fim = time(10, 0)
    dia_semana = DiaSemana.SEGUNDA
    with pytest.raises(ValueError, match="O horário de início deve ser menor do que o horário final"):
        Disponibilidade(id_disponibilidade=id_disponibilidade, hora_inicio=hora_inicio, hora_fim=hora_fim, dia_semana=dia_semana)

def test_disponibilidade_dia_semana_invalido():
    id_disponibilidade = 4
    hora_inicio = time(9, 0)
    hora_fim = time(12, 0)
    dia_semana_invalido = "domingo"  # Valor inválido para DiaSemana
    with pytest.raises(ValueError, match="O dia da semana deve ser um valor de DiaSemana"):
        Disponibilidade(id_disponibilidade=id_disponibilidade, hora_inicio=hora_inicio, hora_fim=hora_fim, dia_semana=dia_semana_invalido)

def test_disponibilidade_dia_semana_valido():
    id_disponibilidade = 5
    hora_inicio = time(9, 0)
    hora_fim = time(12, 0)
    dia_semana_valido = DiaSemana.SEGUNDA  # Valor válido para DiaSemana
    disponibilidade = Disponibilidade(id_disponibilidade=id_disponibilidade, hora_inicio=hora_inicio, hora_fim=hora_fim, dia_semana=dia_semana_valido)
    assert disponibilidade.dia_semana == dia_semana_valido