from datetime import date

from sistema_veterinario.adapters.repository import FakeClienteRepository
from sistema_veterinario.domain.model import Cliente, CPF, Paciente, Telefone
from sistema_veterinario.service_layer.services import adicionar_paciente, buscar_cliente, buscar_paciente, cadastrar_cliente


def criar_cliente_valido(id_cliente: int = 1) -> Cliente:
    return Cliente(
        id_cliente=id_cliente,
        nome="João Silva",
        cpf=CPF(numero="52998224725"),
        telefone=Telefone(numero="11999999999"),
    )


def test_cadastrar_cliente():
    
    repository = FakeClienteRepository()
    
    cadastrar_cliente(
        repository=repository,
        id_cliente=1,
        nome="João Silva",
        cpf="52998224725",
        telefone="11999999999",
    )

    cliente = repository.get(1)

    assert cliente is not None
    assert cliente.id_cliente == 1
    assert cliente.nome == "João Silva"
    assert cliente.cpf.numero == "52998224725"
    assert cliente.telefone.numero == "11999999999"


def test_buscar_cliente():
 
    repository = FakeClienteRepository()
    cliente = criar_cliente_valido(id_cliente=1)
    repository.add(cliente)

    resultado = buscar_cliente(repository, 1)

    assert resultado is not None
    assert resultado.id_cliente == 1
    assert resultado.nome == "João Silva"
    assert resultado.cpf.numero == "52998224725"
    assert resultado.telefone.numero == "11999999999"


def test_adicionar_paciente():
    
    repository = FakeClienteRepository()
    cliente = criar_cliente_valido(id_cliente=1)
    repository.add(cliente)

    
    adicionar_paciente(
        repository=repository,
        id_cliente=1,
        id_paciente=10,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=5,
    )

    
    cliente_atualizado = repository.get(1)

    assert len(cliente_atualizado.pacientes) == 1

    paciente = cliente_atualizado.pacientes[0]
    assert paciente.id_paciente == 10
    assert paciente.nome == "Rex"
    assert paciente.data_nascimento == date(2020, 5, 10)
    assert paciente.raca_id == 5


def test_buscar_paciente():
    # Arrange
    repository = FakeClienteRepository()
    cliente = criar_cliente_valido(id_cliente=1)

    paciente = Paciente(
        id_paciente=10,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=5,
    )

    cliente.adicionar_paciente(paciente)
    repository.add(cliente)

    
    resultado = buscar_paciente(repository, 1, 10)

    
    assert resultado is not None
    assert resultado.id_paciente == 10
    assert resultado.nome == "Rex"
    assert resultado.data_nascimento == date(2020, 5, 10)
    assert resultado.raca_id == 5