from sistema_veterinario.adapters.repository import FakeVeterinarioRepository
from sistema_veterinario.domain.model import Veterinario


def test_fake_repository_salva_e_busca_veterinario():
    repository = FakeVeterinarioRepository()

    veterinario = Veterinario(
        id_veterinario=1,
        email="carlos@example.com",
        senha_hash="hash123",
        nome="Dr. Carlos",
        crmv="12345",
        especialidade="Neurologista"
    )

    repository.add(veterinario)
    resultado = repository.get(1)

    assert resultado is not None
    assert resultado.id_veterinario == 1
    assert resultado.email == "carlos@example.com"
    assert resultado.senha_hash == "hash123"
    assert resultado.nome == "Dr. Carlos"
    assert resultado.crmv == "12345"
    assert resultado.especialidade == "Neurologista"

def test_fake_repository_busca_veterinario_inexistente():
    repository = FakeVeterinarioRepository()
    resultado = repository.get(999) 
    assert resultado is None