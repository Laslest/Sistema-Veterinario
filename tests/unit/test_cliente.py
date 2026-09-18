from datetime import date

import pytest

from sistema_veterinario.domain.model import (
    Cliente,
    Endereco,
    CPF,
    Paciente,
    Telefone,
)

def criar_cpf_valido():
    return CPF(numero="52998224725")

def criar_telefone_valido():
    return Telefone(numero="11999999999")

def criar_endereco_valido():
    return Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000",
    )

def criar_paciente_valido(id_paciente: int = 1):
    return Paciente(
        id_paciente=id_paciente,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=10,
    )

def criar_cliente_valido(id_cliente: int = 1) -> Cliente:
    return Cliente(
        id_cliente=id_cliente,
        nome="João Silva",
        cpf=criar_cpf_valido(),
        telefone=criar_telefone_valido(),
        endereco=criar_endereco_valido(),
    )

def test_cliente_valido_e_criado_com_sucesso():
    cliente = criar_cliente_valido()

    assert cliente.id_cliente == 1
    assert cliente.nome == "João Silva"
    assert cliente.pacientes == []

def test_cliente_com_id_zero_gera_erro():
    with pytest.raises(ValueError, match="ID do cliente"):
        Cliente(
            id_cliente=0,
            nome="João Silva",
            cpf=criar_cpf_valido(),
            telefone=criar_telefone_valido(),
            endereco=criar_endereco_valido(),
        )

def test_cliente_com_nome_vazio_gera_erro():
    with pytest.raises(ValueError, match="nome do cliente não pode ser vazio"):
        Cliente(
            id_cliente=1,
            nome="",
            cpf=criar_cpf_valido(),
            telefone=criar_telefone_valido(),
            endereco=criar_endereco_valido(),
        )

def test_adicionar_paciente_ao_cliente_com_sucesso():
    cliente = criar_cliente_valido()
    paciente = criar_paciente_valido(id_paciente=1)

    cliente.adicionar_paciente(paciente)

    assert len(cliente.pacientes) == 1
    assert cliente.pacientes[0].id_paciente == 1

def test_nao_permite_adicionar_paciente_duplicado():
    cliente = criar_cliente_valido()
    paciente = criar_paciente_valido(id_paciente=1)
    cliente.adicionar_paciente(paciente)

    with pytest.raises(ValueError, match="já está cadastrado"):
        cliente.adicionar_paciente(paciente)

def test_buscar_paciente_existente_retorna_paciente():
    cliente = criar_cliente_valido()
    paciente = criar_paciente_valido(id_paciente=42)
    cliente.adicionar_paciente(paciente)

    encontrado = cliente.buscar_paciente(42)

    assert encontrado.id_paciente == 42

def test_buscar_paciente_inexistente_gera_erro():
    cliente = criar_cliente_valido()

    with pytest.raises(ValueError, match="não encontrado"):
        cliente.buscar_paciente(99)

def test_remover_paciente_existente_com_sucesso():
    cliente = criar_cliente_valido()
    paciente = criar_paciente_valido(id_paciente=42)
    cliente.adicionar_paciente(paciente)

    cliente.remover_paciente(42)

    assert len(cliente.pacientes) == 0

def test_remover_paciente_inexistente_gera_erro():
    cliente = criar_cliente_valido()

    with pytest.raises(ValueError, match="não encontrado"):
        cliente.remover_paciente(99)

def test_dois_clientes_com_mesmo_id_sao_iguais():
    cliente1 = criar_cliente_valido(id_cliente=1)
    cliente2 = Cliente(
        id_cliente=1,
        nome="Maria Souza",
        cpf=CPF(numero="11144477735"),
        telefone=Telefone(numero="21988888888"),
        endereco=Endereco(
            rua="Rua B",
            numero="200",
            bairro="Icaraí",
            cidade="Niterói",
            estado="RJ",
            cep="24200000",
        ),
    )

    assert cliente1 == cliente2

def test_dois_clientes_com_ids_diferentes_nao_sao_iguais():
    cliente1 = criar_cliente_valido(id_cliente=1)
    cliente2 = criar_cliente_valido(id_cliente=2)

    assert cliente1 != cliente2