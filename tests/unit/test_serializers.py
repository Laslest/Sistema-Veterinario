from sistema_veterinario.domain.model import Endereco, Unidade
from sistema_veterinario.entrypoints.serializers import serializar_unidade


def test_serializar_unidade_com_endereco():
    endereco = Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000",
    )
    unidade = Unidade(
        id_unidade=101,
        nome="Clínica Central",
        endereco=endereco,
        atende_domicilio=False,
    )

    assert serializar_unidade(unidade) == {
        "id_unidade": 101,
        "nome": "Clínica Central",
        "atende_domicilio": False,
        "endereco": {
            "rua": "Rua A",
            "numero": "100",
            "bairro": "Centro",
            "cidade": "Niterói",
            "estado": "RJ",
            "cep": "24000000",
        },
    }


def test_serializar_unidade_domiciliar_sem_endereco():
    unidade = Unidade(
        id_unidade=103,
        nome="Atendimento Móvel",
        endereco=None,
        atende_domicilio=True,
    )

    assert serializar_unidade(unidade) == {
        "id_unidade": 103,
        "nome": "Atendimento Móvel",
        "atende_domicilio": True,
        "endereco": None,
    }
