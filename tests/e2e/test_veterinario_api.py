from sistema_veterinario.entrypoints.flask_app import create_app


def test_cadastrar_veterinario_api():
    app = create_app("sqlite:///:memory:")
    client = app.test_client()

    response = client.post(
        "/veterinarios",
        json={
            "id_veterinario": 1,
            "email": "veterinario@example.com",
            "senha_hash": "hashed_password",
            "nome": "Veterinário Exemplo",
            "crmv": "CRMV-12345",
            "especialidade": "Clínica Geral",
        },
    )

    dados = response.get_json()

    assert response.status_code == 201
    assert dados["id_veterinario"] == 1
    assert dados["email"] == "veterinario@example.com"
    assert dados["nome"] == "Veterinário Exemplo"
    assert dados["crmv"] == "CRMV-12345"
    assert dados["especialidade"] == "Clínica Geral"
    assert "senha_hash" not in dados

def test_buscar_veterinario_api():
    app = create_app("sqlite:///:memory:")
    client = app.test_client()

    # Primeiro, cadastramos um veterinário
    client.post(
        "/veterinarios",
        json={
            "id_veterinario": 1,
            "email": "veterinario@example.com",
            "senha_hash": "hashed_password",
            "nome": "Veterinário Exemplo",
            "crmv": "CRMV-12345",
            "especialidade": "Clínica Geral",
        },
    )

    # Agora, buscamos o veterinário cadastrado
    response = client.get("/veterinarios/1")

    dados = response.get_json()

    assert response.status_code == 200
    assert dados["id_veterinario"] == 1
    assert dados["email"] == "veterinario@example.com"
    assert dados["nome"] == "Veterinário Exemplo"
    assert dados["crmv"] == "CRMV-12345"
    assert dados["especialidade"] == "Clínica Geral"
    assert "senha_hash" not in dados
    assert dados["disponibilidades"] == []

def test_adicionar_disponibilidade_veterinario_api():
    app = create_app("sqlite:///:memory:")
    client = app.test_client()

    # Primeiro, cadastramos um veterinário
    client.post(
        "/veterinarios",
        json={
            "id_veterinario": 1,
            "email": "veterinario@example.com",
            "senha_hash": "hashed_password",
            "nome": "Veterinário Exemplo",
            "crmv": "CRMV-12345",
            "especialidade": "Clínica Geral",
        },
    )

    # Agora, adicionamos uma disponibilidade para o veterinário
    response = client.post(
        "/veterinarios/1/disponibilidades",
        json={
            "id_disponibilidade": 1,
            "dia_semana": "segunda",
            "hora_inicio": "09:00:00",
            "hora_fim": "12:00:00",
        },
    )

    dados = response.get_json()

    assert response.status_code == 201
    assert dados["id_disponibilidade"] == 1
    assert dados["dia_semana"] == "segunda"
    assert dados["hora_inicio"] == "09:00:00"
    assert dados["hora_fim"] == "12:00:00"

    response_busca = client.get("/veterinarios/1")
    dados_busca = response_busca.get_json()

    assert response_busca.status_code == 200
    assert len(dados_busca["disponibilidades"]) == 1
    assert dados_busca["disponibilidades"][0]["id_disponibilidade"] == 1
    assert dados_busca["disponibilidades"][0]["dia_semana"] == "segunda"
    assert dados_busca["disponibilidades"][0]["hora_inicio"] == "09:00:00"
    assert dados_busca["disponibilidades"][0]["hora_fim"] == "12:00:00"