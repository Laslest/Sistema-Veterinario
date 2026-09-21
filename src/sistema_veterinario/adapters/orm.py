from sqlalchemy import Column, DateTime, Integer, String, Table
from sqlalchemy.orm import registry

from sistema_veterinario.domain.model import Agendamento


mapper_registry = registry()
metadata = mapper_registry.metadata


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
        Agendamento,
        agendamentos,
    )