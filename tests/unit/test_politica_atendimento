import pytest

from sistema_veterinario.domain.model import (Endereco, Unidade, AtendimentoPresencial, AtendimentoDomiciliar)


def criar_endereco():
    return Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000",
    )


def test_atendimento_presencial_rejeita_endereco_ausente():
    politica = AtendimentoPresencial()

    with pytest.raises(
        ValueError,
        match="Unidade física precisa de um endereço",
    ):
        politica.validar_endereco(None)


def test_atendimento_presencial_aceita_endereco_informado():
    politica = AtendimentoPresencial()

    politica.validar_endereco(criar_endereco())


def test_atendimento_domiciliar_aceita_endereco_ausente():
    politica = AtendimentoDomiciliar()

    politica.validar_endereco(None)


def test_atendimento_domiciliar_aceita_endereco_informado():
    politica = AtendimentoDomiciliar()

    politica.validar_endereco(criar_endereco())


@pytest.mark.parametrize(
    ("atende_domicilio", "tipo_esperado"),
    [
        (False, AtendimentoPresencial),
        (True, AtendimentoDomiciliar),
    ],
)
def test_unidade_seleciona_politica_de_atendimento(
    atende_domicilio,
    tipo_esperado,
):
    endereco = None if atende_domicilio else criar_endereco()

    unidade = Unidade(
        id_unidade=1,
        nome="Clínica Veterinária",
        endereco=endereco,
        atende_domicilio=atende_domicilio,
    )

    assert isinstance(unidade.politica_atendimento, tipo_esperado)