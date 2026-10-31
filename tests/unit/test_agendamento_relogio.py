from datetime import datetime, timedelta

import pytest

from sistema_veterinario.adapters.repository import FakeAgendamentoRepository
from sistema_veterinario.domain.model import Agendamento, Relogio
from sistema_veterinario.service_layer.services import criar_agendamento


class RelogioFixo(Relogio):

    def __init__(self, instante):
        self.instante = instante

    def agora(self):
        return self.instante


AGORA = datetime(2026, 10, 30, 22, 0)


def criar(data_hora, relogio):
    return Agendamento(
        id_agendamento=1,
        id_paciente=1,
        id_veterinario=1,
        id_unidade=1,
        id_tipo_agendamento=1,
        data_hora=data_hora,
        relogio=relogio,
    )


def test_agendamento_usa_o_relogio_recebido():
    agendamento = criar(AGORA + timedelta(minutes=1), RelogioFixo(AGORA))

    assert agendamento.status == "AGENDADO"


def test_nao_permite_agendamento_no_mesmo_instante_do_relogio():
    futuro = datetime(2100, 1, 1, 10, 0)

    with pytest.raises(ValueError):
        criar(futuro, RelogioFixo(futuro))


def test_servico_repassa_o_relogio_para_o_agendamento():
    repository = FakeAgendamentoRepository()

    criar_agendamento(
        repository=repository,
        id_agendamento=1,
        id_paciente=10,
        id_veterinario=20,
        id_unidade=30,
        id_tipo_agendamento=40,
        data_hora=AGORA + timedelta(minutes=1),
        relogio=RelogioFixo(AGORA),
    )

    assert repository.get(1).status == "AGENDADO"
