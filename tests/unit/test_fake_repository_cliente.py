import pytest

from sistema_veterinario.adapters.repository import ClienteJaCadastradoError, FakeClienteRepository
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

def test_fake_repository_nao_substitui_cliente_com_id_duplicado():
    repository = FakeClienteRepository()

    cliente_original = Cliente(
        id_cliente=1,
        nome="João Silva",
        cpf=CPF(numero="52998224725"),
        telefone=Telefone(numero="11999999999"),
    )

    cliente_duplicado = Cliente(
        id_cliente=1,
        nome="Maria Silva",
        cpf=CPF(numero="11144477735"),
        telefone=Telefone(numero="21988888888"),
    )

    repository.add(cliente_original)

    with pytest.raises(ClienteJaCadastradoError):
        repository.add(cliente_duplicado)

    resultado = repository.get(1)

    assert resultado is cliente_original
    assert resultado.nome == "João Silva"