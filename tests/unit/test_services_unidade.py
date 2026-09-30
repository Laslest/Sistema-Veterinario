from sistema_veterinario.adapters.repository import FakeUnidadeRepository
from sistema_veterinario.domain.model import Endereco
from sistema_veterinario.service_layer.services import (cadastrar_unidade, buscar_unidade)


def criar_endereco():
    return Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000",
    )


def test_cadastrar_unidade():
    repository = FakeUnidadeRepository()

    unidade = cadastrar_unidade(
        repository=repository,
        id_unidade=1,
        nome="Clínica A",
        endereco=criar_endereco(),
        atende_domicilio=False,
    )

    assert unidade.id_unidade == 1
    assert unidade.nome == "Clínica A"
    assert unidade.endereco.rua == "Rua A"
    assert unidade.endereco.cep == "24000000"
    assert unidade.atende_domicilio is False

    assert repository.get(1) == unidade


def test_buscar_unidade():
    repository = FakeUnidadeRepository()

    unidade = cadastrar_unidade(
        repository=repository,
        id_unidade=1,
        nome="Clínica A",
        endereco=criar_endereco(),
        atende_domicilio=False,
    )

    resultado = buscar_unidade(
        repository=repository,
        id_unidade=1,
    )

    assert resultado == unidade


def test_buscar_unidade_inexistente():
    repository = FakeUnidadeRepository()

    try:
        buscar_unidade(
            repository=repository,
            id_unidade=999,
        )
        assert False
    except ValueError as erro:
        assert str(erro) == "Unidade não encontrada"