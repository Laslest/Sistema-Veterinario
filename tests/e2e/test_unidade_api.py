from sistema_veterinario.entrypoints.flask_app import create_app


def criar_client():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    return app.test_client()


def test_api_cadastra_unidade_com_endereco():
    client = criar_client()

    resposta = client.post(
        "/unidades",
        json={
            "id_unidade": 101,
            "nome": "Clínica Veterinária Central",
            "atende_domicilio": False,
            "endereco": {
                "rua": "Rua A",
                "numero": "100",
                "bairro": "Centro",
                "cidade": "Niterói",
                "estado": "RJ",
                "cep": "24000000",
            },
        },
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["id_unidade"] == 101
    assert dados["nome"] == "Clínica Veterinária Central"
    assert dados["atende_domicilio"] is False

    assert dados["endereco"]["rua"] == "Rua A"
    assert dados["endereco"]["numero"] == "100"
    assert dados["endereco"]["bairro"] == "Centro"
    assert dados["endereco"]["cidade"] == "Niterói"
    assert dados["endereco"]["estado"] == "RJ"
    assert dados["endereco"]["cep"] == "24000000"


def test_api_busca_unidade():
    client = criar_client()

    resposta_criacao = client.post(
        "/unidades",
        json={
            "id_unidade": 102,
            "nome": "Clínica B",
            "atende_domicilio": False,
            "endereco": {
                "rua": "Rua B",
                "numero": "200",
                "bairro": "Icaraí",
                "cidade": "Niterói",
                "estado": "RJ",
                "cep": "24230000",
            },
        },
    )

    assert resposta_criacao.status_code == 201

    resposta = client.get("/unidades/102")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["id_unidade"] == 102
    assert dados["nome"] == "Clínica B"
    assert dados["atende_domicilio"] is False

    assert dados["endereco"]["rua"] == "Rua B"
    assert dados["endereco"]["numero"] == "200"
    assert dados["endereco"]["bairro"] == "Icaraí"
    assert dados["endereco"]["cidade"] == "Niterói"
    assert dados["endereco"]["estado"] == "RJ"
    assert dados["endereco"]["cep"] == "24230000"


def test_api_busca_unidade_inexistente():
    client = criar_client()

    resposta = client.get("/unidades/999")

    assert resposta.status_code == 404

    dados = resposta.get_json()

    assert dados["erro"] == "Unidade não encontrada"


def test_api_cadastra_unidade_domiciliar_sem_endereco():
    client = criar_client()

    resposta = client.post(
        "/unidades",
        json={
            "id_unidade": 103,
            "nome": "Atendimento Veterinário Móvel",
            "atende_domicilio": True,
            "endereco": None,
        },
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["id_unidade"] == 103
    assert dados["nome"] == "Atendimento Veterinário Móvel"
    assert dados["atende_domicilio"] is True
    assert dados["endereco"] is None