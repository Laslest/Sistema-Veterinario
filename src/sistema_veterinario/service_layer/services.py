from sistema_veterinario.domain.model import Agendamento, Cliente, CPF, Paciente, Telefone


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



def cadastrar_cliente(repository, id_cliente, nome, cpf, telefone):
    cliente = Cliente(
        id_cliente=id_cliente,
        nome=nome,
        cpf=CPF(numero=cpf),
        telefone=Telefone(numero=telefone),
    )

    repository.add(cliente)

    return cliente


def buscar_cliente(repository, id_cliente):
    cliente = repository.get(id_cliente)

    if cliente is None:
        raise ValueError("Cliente não encontrado")

    return cliente


def adicionar_paciente(repository, id_cliente, id_paciente, nome, data_nascimento, raca_id):
    cliente = repository.get(id_cliente)

    if cliente is None:
        raise ValueError("Cliente não encontrado")

    paciente = Paciente(
        id_paciente=id_paciente,
        nome=nome,
        data_nascimento=data_nascimento,
        raca_id=raca_id,
    )

    cliente.adicionar_paciente(paciente)

    return paciente


def remover_paciente(repository, id_cliente, id_paciente):
    cliente = repository.get(id_cliente)

    if cliente is None:
        raise ValueError("Cliente não encontrado")

    cliente.remover_paciente(id_paciente)

    return cliente