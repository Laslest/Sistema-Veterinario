from datetime import date, timedelta

import pytest

from sistema_veterinario.domain.model import Paciente

def test_paciente_valido_e_criado_com_sucesso():
    # Preparação
    id_paciente = 1
    nome = "Rex"
    data_nascimento = date(2020, 5, 10)
    raca_id = 10

    # Execução
    paciente = Paciente(
        id_paciente=id_paciente,
        nome=nome,
        data_nascimento=data_nascimento,
        raca_id=raca_id,
    )

    # Verificação
    assert paciente.id_paciente == 1
    assert paciente.nome == "Rex"
    assert paciente.data_nascimento == date(2020, 5, 10)
    assert paciente.raca_id == 10

def test_paciente_com_id_zero_gera_erro():
    # Preparação
    id_paciente = 0

    # Execução e verificação
    with pytest.raises(ValueError, match="ID do paciente"):
        Paciente(
            id_paciente=id_paciente,
            nome="Rex",
            data_nascimento=date(2020, 5, 10),
            raca_id=10,
        )

def test_paciente_com_nome_vazio_gera_erro():
    # Preparação
    nome = ""

    # Execução e verificação
    with pytest.raises(ValueError, match="nome do paciente não pode ser vazio"):
        Paciente(
            id_paciente=1,
            nome=nome,
            data_nascimento=date(2020, 5, 10),
            raca_id=10,
        )

def test_paciente_com_data_de_nascimento_no_futuro_gera_erro():
    # Preparação
    data_futura = date.today() + timedelta(days=1)

    # Execução e verificação
    with pytest.raises(ValueError, match="não pode estar no futuro"):
        Paciente(
            id_paciente=1,
            nome="Rex",
            data_nascimento=data_futura,
            raca_id=10,
        )

def test_paciente_com_raca_id_zero_gera_erro():
    # Preparação
    raca_id = 0

    # Execução e verificação
    with pytest.raises(ValueError, match="ID da raça"):
        Paciente(
            id_paciente=1,
            nome="Rex",
            data_nascimento=date(2020, 5, 10),
            raca_id=raca_id,
        )

def test_dois_pacientes_com_mesmo_id_sao_iguais():
    # Preparação
    paciente1 = Paciente(
        id_paciente=1,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=10,
    )
    paciente2 = Paciente(
        id_paciente=1,
        nome="Totó",
        data_nascimento=date(2021, 1, 1),
        raca_id=20,
    )

    # Execução e verificação
    assert paciente1 == paciente2

def test_paciente_nao_e_igual_a_objeto_de_outro_tipo():
    # Preparação
    paciente = Paciente(
        id_paciente=1,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=10,
    )

    # Execução e verificação
    assert paciente != "Rex"
    assert paciente != 1
    assert paciente is not None