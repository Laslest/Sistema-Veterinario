from datetime import date, datetime, time

from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from sistema_veterinario.domain.model import Endereco, DiaSemana
from sistema_veterinario.adapters.orm import metadata, start_mappers
from sistema_veterinario.adapters.repository import SqlAlchemyAgendamentoRepository, SqlAlchemyClienteRepository, SqlAlchemyUnidadeRepository, SqlAlchemyVeterinarioRepository
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

    
    @app.route("/clientes", methods=["POST"])
    def cadastrar_cliente_endpoint():
        session = Session()

        try:
            dados = request.get_json(silent=True)

            if dados is None:
                raise ValueError("JSON inválido")

            repository = SqlAlchemyClienteRepository(session)

            cliente = services.cadastrar_cliente(
                repository=repository,
                id_cliente=dados["id_cliente"],
                nome=dados["nome"],
                cpf=dados["cpf"],
                telefone=dados["telefone"],
            )

            session.commit()

            return jsonify(
                {
                    "id_cliente": cliente.id_cliente,
                    "nome": cliente.nome,
                    "cpf": cliente.cpf.numero,
                    "telefone": cliente.telefone.numero,
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
                    "erro": "Cliente já cadastrado ou dados inválidos",
                }
            ), 409

        finally:
            session.close()

    @app.route("/clientes/<int:id_cliente>", methods=["GET"])
    def buscar_cliente_endpoint(id_cliente):
        session = Session()

        try:
            repository = SqlAlchemyClienteRepository(session)

            cliente = services.buscar_cliente(
                repository=repository,
                id_cliente=id_cliente,
            )

            return jsonify(
                {
                    "id_cliente": cliente.id_cliente,
                    "nome": cliente.nome,
                    "cpf": cliente.cpf.numero,
                    "telefone": cliente.telefone.numero,
                    "pacientes": [
                        {
                            "id_paciente": paciente.id_paciente,
                            "nome": paciente.nome,
                            "data_nascimento": (
                                paciente.data_nascimento.isoformat()
                            ),
                            "raca_id": paciente.raca_id,
                        }
                        for paciente in cliente.pacientes
                    ],
                }
            ), 200

        except ValueError as erro:
            if str(erro) == "Cliente não encontrado":
                return jsonify(
                    {
                        "erro": str(erro),
                    }
                ), 404

            return jsonify(
                {
                    "erro": str(erro),
                }
            ), 400

        finally:
            session.close()

    @app.route(
        "/clientes/<int:id_cliente>/pacientes",
        methods=["POST"],
    )
    def adicionar_paciente_endpoint(id_cliente):
        session = Session()

        try:
            dados = request.get_json(silent=True)

            if dados is None:
                raise ValueError("JSON inválido")

            data_nascimento = date.fromisoformat(
                dados["data_nascimento"]
            )

            repository = SqlAlchemyClienteRepository(session)

            paciente = services.adicionar_paciente(
                repository=repository,
                id_cliente=id_cliente,
                id_paciente=dados["id_paciente"],
                nome=dados["nome"],
                data_nascimento=data_nascimento,
                raca_id=dados["raca_id"],
            )

            session.commit()

            return jsonify(
                {
                    "id_paciente": paciente.id_paciente,
                    "nome": paciente.nome,
                    "data_nascimento": (
                        paciente.data_nascimento.isoformat()
                    ),
                    "raca_id": paciente.raca_id,
                }
            ), 201

        except ValueError as erro:
            session.rollback()

            if str(erro) == "Cliente não encontrado":
                return jsonify(
                    {
                        "erro": str(erro),
                    }
                ), 404

            return jsonify(
                {
                    "erro": str(erro),
                }
            ), 400

        except (KeyError, TypeError) as erro:
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
                    "erro": "Paciente já cadastrado ou dados inválidos",
                }
            ), 409

        finally:
            session.close()

    @app.route("/unidades", methods=["POST"])
    def cadastrar_unidade_endpoint():
        session = Session()

        try:
            dados = request.get_json(silent=True)

            if dados is None:
                raise ValueError("JSON inválido")

            endereco = None

            if dados.get("endereco") is not None:
                dados_endereco = dados["endereco"]

                endereco = Endereco(
                    rua=dados_endereco["rua"],
                    numero=dados_endereco["numero"],
                    bairro=dados_endereco["bairro"],
                    cidade=dados_endereco["cidade"],
                    estado=dados_endereco["estado"],
                    cep=dados_endereco["cep"],
                )

            repository = SqlAlchemyUnidadeRepository(session)

            unidade = services.cadastrar_unidade(
                repository=repository,
                id_unidade=dados["id_unidade"],
                nome=dados["nome"],
                endereco=endereco,
                atende_domicilio=dados["atende_domicilio"],
            )

            session.commit()

            return jsonify(
                {
                    "id_unidade": unidade.id_unidade,
                    "nome": unidade.nome,
                    "atende_domicilio": unidade.atende_domicilio,
                    "endereco": (
                        {
                            "rua": unidade.endereco.rua,
                            "numero": unidade.endereco.numero,
                            "bairro": unidade.endereco.bairro,
                            "cidade": unidade.endereco.cidade,
                            "estado": unidade.endereco.estado,
                            "cep": unidade.endereco.cep,
                        }
                        if unidade.endereco is not None
                        else None
                    ),
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
                    "erro": "Unidade já cadastrada ou dados inválidos",
                }
            ), 409

        finally:
            session.close()


    @app.route("/unidades/<int:id_unidade>", methods=["GET"])
    def buscar_unidade_endpoint(id_unidade):
        session = Session()

        try:
            repository = SqlAlchemyUnidadeRepository(session)

            unidade = services.buscar_unidade(
                repository=repository,
                id_unidade=id_unidade,
            )

            return jsonify(
                {
                    "id_unidade": unidade.id_unidade,
                    "nome": unidade.nome,
                    "atende_domicilio": unidade.atende_domicilio,
                    "endereco": (
                        {
                            "rua": unidade.endereco.rua,
                            "numero": unidade.endereco.numero,
                            "bairro": unidade.endereco.bairro,
                            "cidade": unidade.endereco.cidade,
                            "estado": unidade.endereco.estado,
                            "cep": unidade.endereco.cep,
                        }
                        if unidade.endereco is not None
                        else None
                    ),
                }
            ), 200

        except ValueError as erro:
            if str(erro) == "Unidade não encontrada":
                return jsonify(
                    {
                        "erro": str(erro),
                    }
                ), 404

            return jsonify(
                {
                    "erro": str(erro),
                }
            ), 400

        finally:
            session.close()

    @app.route("/veterinarios", methods=["POST"])
    def cadastrar_veterinario_endpoint():
        session = Session()

        try:
            dados = request.get_json(silent=True)

            if dados is None:
                raise ValueError("JSON inválido")

            repository = SqlAlchemyVeterinarioRepository(session)

            veterinario = services.cadastrar_veterinario(
                repository=repository,
                id_veterinario=dados["id_veterinario"],
                email=dados["email"],
                senha_hash=dados["senha_hash"],
                nome=dados["nome"],
                crmv=dados["crmv"],
                especialidade=dados["especialidade"],
            )

            session.commit()

            return jsonify(
                {
                    "id_veterinario": veterinario.id_veterinario,
                    "email": veterinario.email,
                    "nome": veterinario.nome,
                    "crmv": veterinario.crmv,
                    "especialidade": veterinario.especialidade,
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
                    "erro": "Veterinário já cadastrado ou dados inválidos",
                }
            ), 409

        finally:
            session.close()

    @app.route("/veterinarios/<int:id_veterinario>", methods=["GET"])
    def buscar_veterinario_endpoint(id_veterinario):
        session = Session()

        try:
            repository = SqlAlchemyVeterinarioRepository(session)

            veterinario = services.buscar_veterinario(
                repository=repository,
                id_veterinario=id_veterinario,
            )

            return jsonify(
                {
                    "id_veterinario": veterinario.id_veterinario,
                    "email": veterinario.email,
                    "nome": veterinario.nome,
                    "crmv": veterinario.crmv,
                    "especialidade": veterinario.especialidade,
        "disponibilidades": [
                        {
                        "id_disponibilidade": disponibilidade.id_disponibilidade,
                        "dia_semana": disponibilidade.dia_semana.value,
                        "hora_inicio": disponibilidade.hora_inicio.isoformat(),
                        "hora_fim": disponibilidade.hora_fim.isoformat(),
                        }
                        for disponibilidade in veterinario.disponibilidades
                    ],
                }
            ), 200

        except ValueError as erro:
            if str(erro) == "Veterinário não encontrado":
                return jsonify(
                    {
                        "erro": str(erro),
                    }
                ), 404

            return jsonify(
                {
                    "erro": str(erro),
                }
            ), 400

        finally:
            session.close()

    @app.route(
        "/veterinarios/<int:id_veterinario>/disponibilidades",
        methods=["POST"],
    )
    def criar_disponibilidade_endpoint(id_veterinario):
        session = Session()

        try:
            data = request.get_json(silent=True)

            if data is None:
                raise ValueError("JSON inválido")
            
            dia_semana = DiaSemana(data["dia_semana"])
            hora_inicio = time.fromisoformat(data["hora_inicio"])
            hora_fim = time.fromisoformat(data["hora_fim"])

            repository = SqlAlchemyVeterinarioRepository(session)

            disponibilidade = services.adicionar_disponibilidade_veterinario(
                repository=repository,
                id_veterinario=id_veterinario,
                id_disponibilidade=data["id_disponibilidade"],
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
            )
            session.commit()

            return jsonify(
                {
                    "id_disponibilidade": disponibilidade.id_disponibilidade,
                    "dia_semana": disponibilidade.dia_semana.value,
                    "hora_inicio": disponibilidade.hora_inicio.isoformat(),
                    "hora_fim": disponibilidade.hora_fim.isoformat(),
                }
            ), 201

        except (ValueError, KeyError, TypeError) as erro:
            session.rollback()

            if str(erro) == "Veterinário não encontrado":
                status_code = 404
            else:
                status_code = 400

            return jsonify(
                {
                "erro": str(erro),
                }
            ), status_code

        except IntegrityError:
            session.rollback()

            return jsonify(
                {
                    "erro": "Disponibilidade já cadastrada ou dados inválidos",
                }
            ), 409

        finally:
            session.close()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)