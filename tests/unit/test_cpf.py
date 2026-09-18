import pytest

from sistema_veterinario.domain.model import CPF

def test_cpf_valido_e_criado_com_sucesso():
    # Preparação
    numero = "52998224725"

    # Execução
    cpf = CPF(numero=numero)

    # Verificação
    assert cpf.numero == "52998224725"

def test_cpf_com_menos_de_11_digitos_gera_erro():
    # Preparação
    numero = "123456789"

    # Execução e verificação
    with pytest.raises(ValueError, match="Deve conter exatamente 11 dígitos"):
        CPF(numero=numero)

def test_cpf_com_letras_gera_erro():
    # Preparação
    numero = "123456789AB"

    # Execução e verificação
    with pytest.raises(ValueError, match="Deve conter exatamente 11 dígitos"):
        CPF(numero=numero)

def test_cpf_com_todos_os_digitos_iguais_gera_erro():
    # Preparação
    numero = "11111111111"

    # Execução e verificação
    with pytest.raises(ValueError, match="Não pode conter todos os dígitos iguais"):
        CPF(numero=numero)

def test_cpf_com_primeiro_digito_verificador_errado_gera_erro():
    # Preparação
    # CPF base válido "52998224725", alterando o 10º dígito (2 -> 0)
    numero = "52998224705"

    # Execução e verificação
    with pytest.raises(ValueError, match="CPF inválido"):
        CPF(numero=numero)