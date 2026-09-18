import pytest

from sistema_veterinario.domain.model import Endereco, Unidade


def test_criar_endereco_valido_nao_gera_erro():
    # Preparação
    rua = "Rua A"
    numero = "100"
    bairro = "Centro"
    cidade = "Niterói"
    estado = "RJ"
    cep = "24000000"

    # Execução
    endereco = Endereco(
        rua=rua,
        numero=numero,
        bairro=bairro,
        cidade=cidade,
        estado=estado,
        cep=cep
    )

    # Verificação
    assert endereco.rua == "Rua A"
    assert endereco.numero == "100"
    assert endereco.bairro == "Centro"
    assert endereco.cidade == "Niterói"
    assert endereco.estado == "RJ"
    assert endereco.cep == "24000000"


def test_endereco_sem_rua_gera_erro():
    # Preparação
    rua = ""
    numero = "100"
    bairro = "Centro"
    cidade = "Niterói"
    estado = "RJ"
    cep = "24000000"

    # Execução e verificação
    with pytest.raises(ValueError):
        Endereco(
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep
        )


def test_endereco_com_cep_invalido_gera_erro():
    # Preparação
    rua = "Rua A"
    numero = "100"
    bairro = "Centro"
    cidade = "Niterói"
    estado = "RJ"
    cep = "123"

    # Execução e verificação
    with pytest.raises(ValueError):
        Endereco(
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep
        )


def test_unidade_com_nome_vazio_gera_erro():
    # Preparação
    endereco = Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000"
    )

    nome = ""
    atende_domicilio = False

    # Execução e verificação
    with pytest.raises(ValueError):
        Unidade(
            id_unidade=1,
            nome=nome,
            endereco=endereco,
            atende_domicilio=atende_domicilio
        )


def test_unidade_fisica_sem_endereco_gera_erro():
    # Preparação
    nome = "Clínica A"
    atende_domicilio = False
    endereco = None

    # Execução e verificação
    with pytest.raises(ValueError):
        Unidade(
            id_unidade=1,
            nome=nome,
            endereco=endereco,
            atende_domicilio=atende_domicilio
        )


def test_unidade_fisica_com_endereco_valido_criada_com_sucesso():
    # Preparação
    endereco = Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000"
    )

    nome = "Clínica A"
    atende_domicilio = False

    # Execução
    unidade = Unidade(
        id_unidade=1,
        nome=nome,
        endereco=endereco,
        atende_domicilio=atende_domicilio
    )

    # Verificação
    assert unidade.nome == "Clínica A"


def test_duas_unidades_com_mesmo_id_sao_iguais():
    # Preparação
    endereco1 = Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000"
    )

    endereco2 = Endereco(
        rua="Rua B",
        numero="200",
        bairro="Icaraí",
        cidade="Niterói",
        estado="RJ",
        cep="24200000"
    )

    unidade1 = Unidade(
        id_unidade=1,
        nome="Clínica A",
        endereco=endereco1,
        atende_domicilio=False
    )

    unidade2 = Unidade(
        id_unidade=1,
        nome="Clínica B",
        endereco=endereco2,
        atende_domicilio=False
    )

    # Execução e verificação
    assert unidade1 == unidade2