from datetime import time
import pytest
from sistema_veterinario.domain.model import Disponibilidade 

def test_disponibilidade_valida():
    inicio = time(9, 0)
    fim = time(12, 0)
    disponibilidade = Disponibilidade(inicio=inicio, fim=fim)
    assert disponibilidade.inicio == inicio
    assert disponibilidade.fim == fim

def test_disponibilidade_invalida():
    inicio = time(14, 0)
    fim = time(12, 0)
    with pytest.raises(ValueError, match="O horário de início deve ser menor do que o horário final"):
        Disponibilidade(inicio=inicio, fim=fim)

def test_disponibilidade_inicio_igual_fim():
    inicio = time(10, 0)
    fim = time(10, 0)
    with pytest.raises(ValueError, match="O horário de início deve ser menor do que o horário final"):
        Disponibilidade(inicio=inicio, fim=fim)