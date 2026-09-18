import pytest

from sistema_veterinario.domain.model import Especie

def test_especie_valida_e_criada_com_sucesso():
    # Preparação
    id_especie = 1
    nome = "Cachorro"

    # Execução
    especie = Especie(id_especie=id_especie, nome=nome)

    # Verificação
    assert especie.id_especie == 1
    assert especie.nome == "Cachorro"

def test_especie_com_id_zero_gera_erro():
    # Preparação
    id_especie = 0
    nome = "Cachorro"

    # Execução e verificação
    with pytest.raises(ValueError, match="ID da espécie"):
        Especie(id_especie=id_especie, nome=nome)

def test_especie_com_nome_vazio_gera_erro():
    # Preparação
    id_especie = 1
    nome = ""

    # Execução e verificação
    with pytest.raises(ValueError, match="nome da espécie não pode ser vazio"):
        Especie(id_especie=id_especie, nome=nome)

def test_duas_especies_com_mesmo_id_sao_iguais():
    # Preparação
    especie1 = Especie(id_especie=1, nome="Cachorro")
    especie2 = Especie(id_especie=1, nome="Canino")

    # Execução e verificação
    assert especie1 == especie2


def test_duas_especies_com_ids_diferentes_nao_sao_iguais():
    # Preparação
    especie1 = Especie(id_especie=1, nome="Cachorro")
    especie2 = Especie(id_especie=2, nome="Cachorro")

    # Execução e verificação
    assert especie1 != especie2

def test_especie_nao_e_igual_a_objeto_de_outro_tipo():
    # Preparação
    especie = Especie(id_especie=1, nome="Cachorro")

    # Execução e verificação
    assert especie != "Cachorro"
    assert especie != 1
    assert especie is not None