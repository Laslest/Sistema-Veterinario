from sqlalchemy import Column, DateTime, Time, Integer, String, Table, ForeignKey
from sqlalchemy.orm import registry
from sistema_veterinario.domain.model import Agendamento, Veterinario

mapper_registry = registry()
metadata = mapper_registry.metadata

veterinarios = Table(
    "veterinarios",
    metadata,
    Column("id_veterinario", Integer, primary_key=True),
    Column("nome", String, nullable=False),
    Column("crmv", String, nullable=False),
)


disponibilidades = Table(
    "disponibilidades",
    metadata,
    Column("id_veterinario", Integer, ForeignKey("veterinarios.id_veterinario"), primary_key=True),
    Column("inicio", Time, primary_key=True),
    Column("fim", Time, primary_key=True)
)

agendamentos = Table(
    "agendamentos",
    metadata,
    Column("id_agendamento", Integer, primary_key=True),
    Column("id_cliente", Integer, nullable=False),
    Column("id_paciente", Integer, nullable=False),
    Column("id_veterinario", Integer, nullable=False),
    Column("data_hora", DateTime, nullable=False),
    Column("status", String, nullable=False),
)


def start_mappers():
    """
    Inicializa o mapeamento ORM das entidades do domínio.
    """
    mapper_registry.map_imperatively(
        Veterinario,
        veterinarios,
    )

    mapper_registry.map_imperatively(
        Agendamento,
        agendamentos,
    )