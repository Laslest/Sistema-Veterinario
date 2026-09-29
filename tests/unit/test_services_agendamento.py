from datetime import datetime, timedelta

from sistema_veterinario.adapters.repository import FakeAgendamentoRepository
from sistema_veterinario.domain.model import Agendamento
from sistema_veterinario.service_layer.services import (
    criar_agendamento,
    cancelar_agendamento,
)


def test_criar_agendamento():
    repository = FakeAgendamentoRepository()

    data_hora = datetime.now() + timedelta(days=1)

    criar_agendamento(
        repository=repository,
        id_agendamento=1,
        id_paciente=10,
        id_veterinario=20,
        id_unidade=30,
        id_tipo_agendamento=40,
        data_hora=data_hora,
    )

    agendamento = repository.get(1)

    assert agendamento is not None
    assert agendamento.id_agendamento == 1
    assert agendamento.id_paciente == 10
    assert agendamento.id_veterinario == 20
    assert agendamento.id_unidade == 30
    assert agendamento.id_tipo_agendamento == 40
    assert agendamento.data_hora == data_hora
    assert agendamento.status == "AGENDADO"


def test_cancelar_agendamento():
    repository = FakeAgendamentoRepository()

    agendamento = Agendamento(
        id_agendamento=1,
        id_paciente=10,
        id_veterinario=20,
        id_unidade=30,
        id_tipo_agendamento=40,
        data_hora=datetime.now() + timedelta(days=1),
    )

    repository.add(agendamento)

    cancelar_agendamento(repository, 1)

    agendamento_cancelado = repository.get(1)

    assert agendamento_cancelado.status == "CANCELADO"