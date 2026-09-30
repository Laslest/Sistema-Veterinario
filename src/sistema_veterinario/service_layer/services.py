from sistema_veterinario.domain.model import Agendamento, Cliente, CPF, Disponibilidade, Paciente, Telefone, Endereco, Unidade, Veterinario


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

def cadastrar_unidade(repository, id_unidade, nome, endereco, atende_domicilio,):
    unidade = Unidade(
        id_unidade=id_unidade,
        nome=nome,
        endereco=endereco,
        atende_domicilio=atende_domicilio,
    )

    repository.add(unidade)

    return unidade

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


def buscar_paciente(repository, id_cliente, id_paciente):
    cliente = repository.get(id_cliente)

    if cliente is None:
        raise ValueError("Cliente não encontrado")

    return cliente.buscar_paciente(id_paciente)

def cadastrar_unidade(repository, id_unidade, nome, endereco, atende_domicilio,):
    unidade = Unidade(
        id_unidade=id_unidade,
        nome=nome,
        endereco=endereco,
        atende_domicilio=atende_domicilio,
    )

    repository.add(unidade)

    return unidade


def buscar_unidade(repository, id_unidade):
    unidade = repository.get(id_unidade)

    if unidade is None:
        raise ValueError("Unidade não encontrada")

    return unidade

def cadastrar_veterinario(repository, id_veterinario, email, senha_hash, nome, crmv, especialidade):

    veterinario = Veterinario(
        id_veterinario=id_veterinario,
        email=email,
        senha_hash=senha_hash,
        nome=nome,
        crmv=crmv,
        especialidade=especialidade,
    )

    repository.add(veterinario)

    return veterinario

def buscar_veterinario(repository, id_veterinario):
    veterinario = repository.get(id_veterinario)

    if veterinario is None:
        raise ValueError("Veterinário não encontrado")

    return veterinario

def adicionar_disponibilidade_veterinario(repository, id_veterinario, id_disponibilidade, dia_semana, hora_inicio, hora_fim):
    veterinario = repository.get(id_veterinario)
    
    if veterinario is None:
        raise ValueError("Veterinário não encontrado")

    disponibilidade = Disponibilidade(
        id_disponibilidade=id_disponibilidade,
        dia_semana=dia_semana, 
        hora_inicio=hora_inicio, 
        hora_fim=hora_fim)

    veterinario.adicionar_disponibilidade(disponibilidade)

    return disponibilidade

