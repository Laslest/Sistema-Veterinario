from datetime import datetime, timedelta

import pytest

from sistema_veterinario.domain.model import Agendamento


def test_agendamento_inicia_com_status_agendado():
    data_futura = datetime.now() + timedelta(days=1)

    agendamento = Agendamento(1, 1, 1, 1, data_futura)

    assert agendamento.status == "AGENDADO"


def test_nao_permite_agendamento_no_passado():
    data_passada = datetime.now() - timedelta(days=1)

    with pytest.raises(ValueError):
        Agendamento(1, 1, 1, 1, data_passada)