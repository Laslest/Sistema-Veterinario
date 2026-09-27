from sistema_veterinario.adapters.repository import FakeClienteRepository
from sistema_veterinario.domain.model import Cliente, CPF, Telefone


def test_fake_repository_salva_e_busca_cliente():
    repository = FakeClienteRepository()

    cliente = Cliente(
        id_cliente=1,
        nome="João Silva",
        cpf=CPF(numero="52998224725"),
        telefone=Telefone(numero="11999999999"),
    )

    repository.add(cliente)

    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_cliente == 1
    assert resultado.nome == "João Silva"
    assert resultado.cpf.numero == "52998224725"
    assert resultado.telefone.numero == "11999999999"


def test_fake_repository_busca_cliente_inexistente():
    repository = FakeClienteRepository()

    resultado = repository.get(999)

    assert resultado is None