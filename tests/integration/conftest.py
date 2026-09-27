import pytest
from sistema_veterinario.adapters.orm import start_mappers


@pytest.fixture(scope="session", autouse=True)
def configurar_mappers():
    start_mappers()