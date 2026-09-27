from sqlalchemy import Column, DateTime, Time, Integer, String, Table, ForeignKey, Date, Boolean, Enum
from sqlalchemy.orm import registry, composite, relationship

from sistema_veterinario.domain.model import Agendamento, Veterinario, Cliente, Paciente, CPF, Telefone, Unidade, Endereco, Disponibilidade, DiaSemana


mapper_registry = registry()
metadata = mapper_registry.metadata


veterinarios = Table(
    "veterinarios",
    metadata,
    Column("id_veterinario", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("senha_hash", String, nullable=False),
    Column("nome", String, nullable=False),
    Column("crmv", String, nullable=False),
    Column("especialidade", String, nullable=False)
)


disponibilidades = Table(
    "disponibilidades",
    metadata,
    Column("id_disponibilidade", Integer, primary_key=True),
    Column(
        "id_veterinario",
        Integer,
        ForeignKey("veterinarios.id_veterinario"),
        nullable=False,
    ),
    Column("dia_semana", Enum(DiaSemana), nullable=False),
    Column("hora_inicio", Time, nullable=False),
    Column("hora_fim", Time, nullable=False),
)


agendamentos = Table(
    "agendamentos",
    metadata,
    Column("id_agendamento", Integer, primary_key=True),
    Column("id_paciente", Integer, nullable=False),
    Column("id_veterinario", Integer, nullable=False),
    Column("id_unidade", Integer, nullable=False),
    Column("id_tipo_agendamento", Integer, nullable=False),
    Column("data_hora", DateTime, nullable=False),
    Column("status", String, nullable=False),
)

clientes = Table(
    "clientes",
    metadata,
    Column("id_cliente", Integer, primary_key=True),
    Column("nome", String, nullable=False),
    Column("cpf_numero", String(11), nullable=False),
    Column("telefone_numero", String(11), nullable=False),
)

pacientes = Table(
    "pacientes",
    metadata,
    Column("id_paciente", Integer, primary_key=True),
    Column("id_cliente", ForeignKey("clientes.id_cliente"), nullable=False),
    Column("nome", String, nullable=False),
    Column("data_nascimento", Date, nullable=False),
    Column("raca_id", Integer, nullable=False),
)

unidades = Table(
    "unidades",
    metadata,
    Column("id_unidade", Integer, primary_key=True),
    Column("nome", String, nullable=False),
    Column("atende_domicilio", Boolean, nullable=False),
    Column("rua", String, nullable=True),
    Column("numero", String, nullable=True),
    Column("bairro", String, nullable=True),
    Column("cidade", String, nullable=True),
    Column("estado", String, nullable=True),
    Column("cep", String, nullable=True),
)

def start_mappers():
    """
    Inicializa o mapeamento ORM das entidades do domínio.
    """

    mapper_registry.map_imperatively(
        Disponibilidade,
        disponibilidades,
    )
    mapper_registry.map_imperatively(
        Veterinario,
        veterinarios,
        properties={
            "disponibilidades": relationship(Disponibilidade, cascade="all, delete-orphan"),
        },
    )

    mapper_registry.map_imperatively(
        Agendamento,
        agendamentos,
    )

    mapper_registry.map_imperatively(
        Paciente,
        pacientes,
        properties={
            "_id_cliente": pacientes.c.id_cliente,
        },
    )

    mapper_registry.map_imperatively(
        Cliente,
        clientes,
        properties={
            "cpf": composite(CPF, clientes.c.cpf_numero),
            "telefone": composite(Telefone, clientes.c.telefone_numero),
            "pacientes": relationship(Paciente),
        },
    )
    mapper_registry.map_imperatively(
        Unidade,
        unidades,
        properties={
            "endereco": composite(
                Endereco,
                unidades.c.rua,
                unidades.c.numero,
                unidades.c.bairro,
                unidades.c.cidade,
                unidades.c.estado,
                unidades.c.cep,
            ),
        },
    )