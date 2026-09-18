import pytest

from sistema_veterinario.domain.model import Telefone

def test_telefone_fixo_valido_e_criado_com_sucesso():
    # Preparação
    numero = "1133334444"

    # Execução
    telefone = Telefone(numero=numero)

    # Verificação
    assert telefone.numero == "1133334444"

def test_telefone_celular_valido_e_criado_com_sucesso():
    # Preparação
    numero = "11999999999"

    # Execução
    telefone = Telefone(numero=numero)

    # Verificação
    assert telefone.numero == "11999999999"

def test_telefone_com_menos_de_10_digitos_gera_erro():
    # Preparação
    numero = "119999999"

    # Execução e verificação
    with pytest.raises(ValueError, match="Deve ter 10"):
        Telefone(numero=numero)

def test_telefone_com_letras_gera_erro():
    # Preparação
    numero = "1199999999A"

    # Execução e verificação
    with pytest.raises(ValueError, match="somente números"):
        Telefone(numero=numero)


def test_telefone_vazio_gera_erro():
    # Preparação
    numero = ""

    # Execução e verificação
    with pytest.raises(ValueError, match="não pode ser vazio"):
        Telefone(numero=numero)

def test_telefone_com_ddd_menor_que_11_gera_erro():
    # Preparação
    numero = "01999999999"

    # Execução e verificação
    with pytest.raises(ValueError, match="DDD deve estar entre 11 e 99"):
        Telefone(numero=numero)

def test_telefone_celular_sem_nove_na_terceira_posicao_gera_erro():
    # Preparação
    # 11 dígitos, mas o 3º dígito (posição 2) não é 9
    numero = "11888888888"

    # Execução e verificação
    with pytest.raises(ValueError, match="começar com '9'"):
        Telefone(numero=numero)