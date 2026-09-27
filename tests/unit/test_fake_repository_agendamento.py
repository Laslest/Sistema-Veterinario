from datetime import datetime, timedelta

from sistema_veterinario.adapters.repository import FakeAgendamentoRepository
from sistema_veterinario.domain.model import Agendamento


def test_fake_repository_adiciona_e_busca_agendamento():
    repository = FakeAgendamentoRepository()

    data_futura = datetime.now() + timedelta(days=1)

    agendamento = Agendamento(
        id_agendamento=1,
        id_paciente=20,
        id_veterinario=30,
        id_unidade=40,
        id_tipo_agendamento=50,
        data_hora=data_futura,
    )

    repository.add(agendamento)

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_agendamento == 1
    assert resultado.id_paciente == 20
    assert resultado.id_veterinario == 30
    assert resultado.id_unidade == 40
    assert resultado.id_tipo_agendamento == 50
    assert resultado.data_hora == data_futura
    assert resultado.status == "AGENDADO"

def test_fake_repository_retorna_none_para_agendamento_inexistente():
    repository = FakeAgendamentoRepository()

    resultado = repository.get(999)

    assert resultado is None