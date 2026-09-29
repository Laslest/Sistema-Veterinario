from datetime import datetime, timedelta

from sistema_veterinario.entrypoints.flask_app import create_app


def criar_client():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    return app.test_client()


def test_api_cria_agendamento():
    client = criar_client()

    data_hora = (datetime.now() + timedelta(days=1)).isoformat()

    resposta = client.post(
        "/agendamentos",
        json={
            "id_agendamento": 101,
            "id_paciente": 10,
            "id_veterinario": 20,
            "id_unidade": 30,
            "id_tipo_agendamento": 40,
            "data_hora": data_hora,
        },
    )

    assert resposta.status_code == 201

    dados = resposta.get_json()

    assert dados["id_agendamento"] == 101
    assert dados["id_paciente"] == 10
    assert dados["id_veterinario"] == 20
    assert dados["id_unidade"] == 30
    assert dados["id_tipo_agendamento"] == 40
    assert dados["status"] == "AGENDADO"


def test_api_cancela_agendamento():
    client = criar_client()

    data_hora = (datetime.now() + timedelta(days=1)).isoformat()

    resposta_criacao = client.post(
        "/agendamentos",
        json={
            "id_agendamento": 102,
            "id_paciente": 10,
            "id_veterinario": 20,
            "id_unidade": 30,
            "id_tipo_agendamento": 40,
            "data_hora": data_hora,
        },
    )

    assert resposta_criacao.status_code == 201

    resposta = client.post(
        "/agendamentos/102/cancelar",
    )

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert dados["id_agendamento"] == 102
    assert dados["status"] == "CANCELADO"