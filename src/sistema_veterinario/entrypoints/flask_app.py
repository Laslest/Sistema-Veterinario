from datetime import datetime

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from sistema_veterinario.adapters.orm import metadata, start_mappers
from sistema_veterinario.adapters.repository import SqlAlchemyAgendamentoRepository
from sistema_veterinario.service_layer import services


def create_app(database_url="sqlite:///sistema_veterinario.db"):
    app = Flask(__name__)

    if database_url == "sqlite:///:memory:":
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        engine = create_engine(database_url)

    start_mappers()
    metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    @app.route("/agendamentos", methods=["POST"])
    def criar_agendamento():
        session = Session()

        try:
            dados = request.get_json(silent=True)

            if dados is None:
                raise ValueError("JSON inválido")

            data_hora = datetime.fromisoformat(dados["data_hora"])

            repository = SqlAlchemyAgendamentoRepository(session)

            agendamento = services.criar_agendamento(
                repository=repository,
                id_agendamento=dados["id_agendamento"],
                id_paciente=dados["id_paciente"],
                id_veterinario=dados["id_veterinario"],
                id_unidade=dados["id_unidade"],
                id_tipo_agendamento=dados["id_tipo_agendamento"],
                data_hora=data_hora,
            )

            session.commit()

            return jsonify(
                {
                    "id_agendamento": agendamento.id_agendamento,
                    "id_paciente": agendamento.id_paciente,
                    "id_veterinario": agendamento.id_veterinario,
                    "id_unidade": agendamento.id_unidade,
                    "id_tipo_agendamento": agendamento.id_tipo_agendamento,
                    "data_hora": agendamento.data_hora.isoformat(),
                    "status": agendamento.status,
                }
            ), 201

        except (ValueError, KeyError, TypeError) as erro:
            session.rollback()

            return jsonify(
                {
                    "erro": str(erro),
                }
            ), 400

        except IntegrityError:
            session.rollback()

            return jsonify(
                {
                    "erro": "Agendamento já cadastrado ou dados inválidos",
                }
            ), 409

        finally:
            session.close()

    @app.route(
        "/agendamentos/<int:id_agendamento>/cancelar",
        methods=["POST"],
    )
    def cancelar_agendamento(id_agendamento):
        session = Session()

        try:
            repository = SqlAlchemyAgendamentoRepository(session)

            agendamento = services.cancelar_agendamento(
                repository=repository,
                id_agendamento=id_agendamento,
            )

            session.commit()

            return jsonify(
                {
                    "id_agendamento": agendamento.id_agendamento,
                    "status": agendamento.status,
                }
            ), 200

        except ValueError as erro:
            session.rollback()

            if str(erro) == "Agendamento não encontrado":
                status_code = 404
            else:
                status_code = 400

            return jsonify(
                {
                    "erro": str(erro),
                }
            ), status_code

        finally:
            session.close()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)