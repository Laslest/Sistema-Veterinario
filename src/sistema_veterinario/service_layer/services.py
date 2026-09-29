from sistema_veterinario.domain.model import Agendamento


def criar_agendamento(
    repository,
    id_agendamento,
    id_paciente,
    id_veterinario,
    id_unidade,
    id_tipo_agendamento,
    data_hora,
):
    agendamento = Agendamento(
        id_agendamento=id_agendamento,
        id_paciente=id_paciente,
        id_veterinario=id_veterinario,
        id_unidade=id_unidade,
        id_tipo_agendamento=id_tipo_agendamento,
        data_hora=data_hora,
    )

    repository.add(agendamento)

    return agendamento


def cancelar_agendamento(repository, id_agendamento):
    agendamento = repository.get(id_agendamento)

    if agendamento is None:
        raise ValueError("Agendamento não encontrado")

    agendamento.cancelar()

    return agendamento