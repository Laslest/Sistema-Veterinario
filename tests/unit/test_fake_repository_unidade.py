from sistema_veterinario.adapters.repository import FakeUnidadeRepository
from sistema_veterinario.domain.model import Endereco, Unidade


def test_fake_repository_salva_e_busca_unidade():
    repository = FakeUnidadeRepository()

    endereco = Endereco(
        rua="Rua A",
        numero="100",
        bairro="Centro",
        cidade="Niterói",
        estado="RJ",
        cep="24000000",
    )

    unidade = Unidade(
        id_unidade=1,
        nome="Clínica A",
        endereco=endereco,
        atende_domicilio=False,
    )

    repository.add(unidade)
    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_unidade == 1
    assert resultado.nome == "Clínica A"
    assert resultado.endereco.rua == "Rua A"
    assert resultado.endereco.cep == "24000000"
    assert resultado.atende_domicilio is False


def test_fake_repository_busca_unidade_inexistente():
    repository = FakeUnidadeRepository()

    resultado = repository.get(999)

    assert resultado is None
