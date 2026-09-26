from datetime import datetime, timedelta

import pytest

from sistema_veterinario.domain.model import Agendamento


def test_agendamento_inicia_com_status_agendado():
    data_futura = datetime.now() + timedelta(days=1)

    agendamento = Agendamento(
        id_agendamento=1,
        id_paciente=1,
        id_veterinario=1,
        id_unidade=1,
        id_tipo_agendamento=1,
        data_hora=data_futura,
    )

    assert agendamento.status == "AGENDADO"


def test_nao_permite_agendamento_no_passado():
    data_passada = datetime.now() - timedelta(days=1)

    with pytest.raises(ValueError):
        Agendamento(
            id_agendamento=1,
            id_paciente=1,
            id_veterinario=1,
            id_unidade=1,
            id_tipo_agendamento=1,
            data_hora=data_passada,
        )