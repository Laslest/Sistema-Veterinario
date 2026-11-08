from datetime import datetime, timedelta

import pytest

from sistema_veterinario.domain.model import (
    Agendamento,
    Cancelado,
    Concluido,
    Confirmado,
)


def criar_agendamento():
    return Agendamento(
        id_agendamento=1,
        id_paciente=1,
        id_veterinario=1,
        id_unidade=1,
        id_tipo_agendamento=1,
        data_hora=datetime.now() + timedelta(days=1),
    )


def test_agendado_pode_ser_confirmado_e_depois_concluido():
    agendamento = criar_agendamento()

    agendamento.confirmar()
    assert agendamento.status == "CONFIRMADO"
    assert isinstance(agendamento.estado, Confirmado)

    agendamento.concluir()
    assert agendamento.status == "CONCLUIDO"
    assert isinstance(agendamento.estado, Concluido)


def test_agendado_pode_ser_cancelado():
    agendamento = criar_agendamento()

    agendamento.cancelar()

    assert agendamento.status == "CANCELADO"
    assert isinstance(agendamento.estado, Cancelado)


@pytest.mark.parametrize(
    "transicoes_anteriores, acao",
    [
        ([], "concluir"),
        (["confirmar"], "confirmar"),
        (["confirmar"], "cancelar"),
        (["cancelar"], "confirmar"),
        (["cancelar"], "cancelar"),
        (["cancelar"], "concluir"),
        (["confirmar", "concluir"], "confirmar"),
        (["confirmar", "concluir"], "cancelar"),
        (["confirmar", "concluir"], "concluir"),
    ],
)
def test_transicao_invalida_gera_erro_e_mantem_o_status(transicoes_anteriores, acao):
    agendamento = criar_agendamento()
    for transicao in transicoes_anteriores:
        getattr(agendamento, transicao)()
    status_antes = agendamento.status

    with pytest.raises(ValueError):
        getattr(agendamento, acao)()

    assert agendamento.status == status_antes
