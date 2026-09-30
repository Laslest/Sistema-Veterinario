from sistema_veterinario.entrypoints.flask_app import create_app


def criar_client():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    return app.test_client()


def test_api_cadastra_cliente():
    client = criar_client()

    resposta = client.post(
        "/clientes",
        json={
            "id_cliente": 1,
            "nome": "João Silva",
            "cpf": "52998224725",
            "telefone": "11999999999",
        },
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["id_cliente"] == 1
    assert dados["nome"] == "João Silva"
    assert dados["cpf"] == "52998224725"
    assert dados["telefone"] == "11999999999"


def test_api_busca_cliente():
    client = criar_client()

    resposta_criacao = client.post(
        "/clientes",
        json={
            "id_cliente": 1,
            "nome": "João Silva",
            "cpf": "52998224725",
            "telefone": "11999999999",
        },
    )

    assert resposta_criacao.status_code == 201

    resposta = client.get("/clientes/1")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["id_cliente"] == 1
    assert dados["nome"] == "João Silva"
    assert dados["cpf"] == "52998224725"
    assert dados["telefone"] == "11999999999"
    assert len(dados["pacientes"]) == 0


def test_api_adiciona_paciente():
    client = criar_client()

    resposta_criacao = client.post(
        "/clientes",
        json={
            "id_cliente": 1,
            "nome": "João Silva",
            "cpf": "52998224725",
            "telefone": "11999999999",
        },
    )

    assert resposta_criacao.status_code == 201

    resposta_paciente = client.post(
        "/clientes/1/pacientes",
        json={
            "id_paciente": 10,
            "nome": "Rex",
            "data_nascimento": "2020-05-10",
            "raca_id": 5,
        },
    )

    assert resposta_paciente.status_code == 201

    dados_paciente = resposta_paciente.get_json()

    assert dados_paciente["id_paciente"] == 10
    assert dados_paciente["nome"] == "Rex"
    assert dados_paciente["data_nascimento"] == "2020-05-10"
    assert dados_paciente["raca_id"] == 5

    resposta_cliente = client.get("/clientes/1")

    assert resposta_cliente.status_code == 200

    dados_cliente = resposta_cliente.get_json()

    assert len(dados_cliente["pacientes"]) == 1

    paciente = dados_cliente["pacientes"][0]

    assert paciente["id_paciente"] == 10
    assert paciente["nome"] == "Rex"
    assert paciente["data_nascimento"] == "2020-05-10"
    assert paciente["raca_id"] == 5