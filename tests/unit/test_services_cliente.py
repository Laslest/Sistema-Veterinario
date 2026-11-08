import pytest
from datetime import date

from sistema_veterinario.adapters.repository import FakeClienteRepository
from sistema_veterinario.domain.model import Cliente, CPF, Telefone, PacienteFactory, PacienteFactoryPadrao
from sistema_veterinario.service_layer.services import adicionar_paciente, buscar_cliente, cadastrar_cliente


def criar_cliente_valido(id_cliente: int = 1) -> Cliente:
    return Cliente(
        id_cliente=id_cliente,
        nome="João Silva",
        cpf=CPF(numero="52998224725"),
        telefone=Telefone(numero="11999999999"),
    )

class PacienteFactoryEspia(PacienteFactory):

    def __init__(self):
        self.chamadas = []

    def criar_paciente(
        self,
        id_paciente,
        nome,
        data_nascimento,
        raca_id,
    ):
        self.chamadas.append(
            (id_paciente, nome, data_nascimento, raca_id)
        )

        return PacienteFactoryPadrao().criar_paciente(
            id_paciente=id_paciente,
            nome=nome,
            data_nascimento=data_nascimento,
            raca_id=raca_id,
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

    
    paciente_criado = adicionar_paciente(
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
    assert paciente_criado is paciente

def test_adicionar_paciente_utiliza_factory_injetada():

    repository = FakeClienteRepository()
    cliente = criar_cliente_valido(id_cliente=1)
    repository.add(cliente)

    factory = PacienteFactoryEspia()

    paciente_criado = adicionar_paciente(
        repository=repository,
        id_cliente=1,
        id_paciente=10,
        nome="Rex",
        data_nascimento=date(2020, 5, 10),
        raca_id=5,
        paciente_factory=factory,
    )

    cliente_atualizado = repository.get(1)

    assert factory.chamadas == [
        (10, "Rex", date(2020, 5, 10), 5)
    ]

    assert paciente_criado is cliente_atualizado.pacientes[0]

def test_adicionar_paciente_com_cliente_inexistente_gera_erro():

    repository = FakeClienteRepository()
    factory = PacienteFactoryEspia()

    with pytest.raises(
        ValueError,
        match="Cliente não encontrado",
    ):
        adicionar_paciente(
            repository=repository,
            id_cliente=999,
            id_paciente=10,
            nome="Rex",
            data_nascimento=date(2020, 5, 10),
            raca_id=5,
            paciente_factory=factory,
        )

    assert factory.chamadas == []