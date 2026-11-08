
from datetime import date, timedelta

import pytest

from sistema_veterinario.domain.model import (
    Paciente,
    PacienteFactoryPadrao,
)


def test_factory_padrao_cria_paciente_valido():
    # Preparação
    factory = PacienteFactoryPadrao()

    # Execução
    paciente = factory.criar_paciente(
        id_paciente=1,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=10,
    )

    # Verificação
    assert isinstance(paciente, Paciente)
    assert paciente.id_paciente == 1
    assert paciente.nome == "Rex"
    assert paciente.data_nascimento == date(2020, 5, 10)
    assert paciente.raca_id == 10


@pytest.mark.parametrize(
    "id_paciente, nome, data_nascimento, raca_id, mensagem",
    [
        (0, "Rex", date(2020, 5, 10), 10, "ID do paciente"),
        (-1, "Rex", date(2020, 5, 10), 10, "ID do paciente"),
        (1, "", date(2020, 5, 10), 10, "nome do paciente"),
        (None, "Rex", date(2020, 5, 10), 10, "ID do paciente"),
        ("abc", "Rex", date(2020, 5, 10), 10, "ID do paciente"),
        (
            1,
            "Rex",
            date.today() + timedelta(days=1),
            10,
            "não pode estar no futuro",
        ),
        (1, "Rex", date(2020, 5, 10), 0, "ID da raça"),
    ],
)
def test_factory_padrao_respeita_validacoes_do_paciente(
    id_paciente,
    nome,
    data_nascimento,
    raca_id,
    mensagem,
):
    factory = PacienteFactoryPadrao()

    with pytest.raises(ValueError, match=mensagem):
        factory.criar_paciente(
            id_paciente=id_paciente,
            nome=nome,
            data_nascimento=data_nascimento,
            raca_id=raca_id,
        )