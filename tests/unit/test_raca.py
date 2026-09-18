import pytest 
 
from sistema_veterinario.domain.model import Raca 
 
def test_raca_valida_e_criada_com_sucesso(): 
    # Preparação 
    id_raca = 10 
    nome = "Labrador" 
    id_especie = 1 
 
    # Execução 
    raca = Raca(id_raca=id_raca, nome=nome, id_especie=id_especie) 
 
    # Verificação 
    assert raca.id_raca == 10 
    assert raca.nome == "Labrador" 
    assert raca.id_especie == 1 
 
def test_raca_com_id_zero_gera_erro(): 
    # Preparação 
    id_raca = 0 
    nome = "Labrador" 
    id_especie = 1 
 
    # Execução e verificação 
    with pytest.raises(ValueError, match="ID da raça"): 
        Raca(id_raca=id_raca, nome=nome, id_especie=id_especie) 
 
def test_raca_com_nome_vazio_gera_erro(): 
    # Preparação 
    id_raca = 10 
    nome = "" 
    id_especie = 1 
 
    # Execução e verificação 
    with pytest.raises(ValueError, match="nome da raça não pode ser vazio"): 
        Raca(id_raca=id_raca, nome=nome, id_especie=id_especie) 
 
 
def test_raca_com_nome_apenas_espacos_gera_erro(): 
    # Preparação 
    id_raca = 10 
    nome = "   " 
    id_especie = 1 
 
    # Execução e verificação 
    with pytest.raises(ValueError, match="nome da raça não pode ser vazio"): 
        Raca(id_raca=id_raca, nome=nome, id_especie=id_especie) 
 
def test_raca_com_id_especie_zero_gera_erro(): 
    # Preparação 
    id_raca = 10 
    nome = "Labrador" 
    id_especie = 0 
 
    # Execução e verificação 
    with pytest.raises(ValueError, match="ID da espécie"): 
        Raca(id_raca=id_raca, nome=nome, id_especie=id_especie) 
 
def test_duas_racas_com_mesmo_id_sao_iguais(): 
    # Preparação 
    raca1 = Raca(id_raca=10, nome="Labrador", id_especie=1) 
    raca2 = Raca(id_raca=10, nome="Golden Retriever", id_especie=1) 
 
    # Execução e verificação 
    assert raca1 == raca2 
 
 
def test_duas_racas_com_ids_diferentes_nao_sao_iguais(): 
    # Preparação 
    raca1 = Raca(id_raca=10, nome="Labrador", id_especie=1) 
    raca2 = Raca(id_raca=11, nome="Labrador", id_especie=1) 
 
    # Execução e verificação 
    assert raca1 != raca2 
 
def test_raca_nao_e_igual_a_objeto_de_outro_tipo(): 
    # Preparação 
    raca = Raca(id_raca=10, nome="Labrador", id_especie=1) 
 
    # Execução e verificação 
    assert raca != "Labrador" 
    assert raca != 10 
    assert raca is not None