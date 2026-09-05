from datetime import datetime

from langchain_core.tools import tool
from sqlalchemy import select

from db.database import get_session
from db.models import Consulta, Horario, Medico

FORMATO_DATA = "%Y-%m-%d %H:%M"


@tool
def consultar_agenda(especialidade: str) -> str:
    """Consulta os horários disponíveis para uma especialidade médica.

    Args:
        especialidade: nome da especialidade, ex: cardiologista, dermatologista.
    """
    especialidade = especialidade.lower().strip()

    with get_session() as session:
        stmt = (
            select(Horario)
            .join(Medico)
            .where(Medico.especialidade == especialidade, Horario.disponivel.is_(True))
            .order_by(Horario.data_hora)
        )
        horarios = session.scalars(stmt).all()

        if not horarios:
            return f"Não encontrei horários disponíveis para {especialidade}."

        lista = ", ".join(h.data_hora.strftime(FORMATO_DATA) for h in horarios)
        return f"Horários disponíveis para {especialidade}: {lista}."


@tool
def marcar_consulta(especialidade: str, horario: str, nome_paciente: str) -> str:
    """Marca uma consulta em um horário específico para um paciente.

    Args:
        especialidade: especialidade médica escolhida.
        horario: horário exato escolhido, no formato AAAA-MM-DD HH:MM.
        nome_paciente: nome do paciente que está marcando a consulta.
    """
    especialidade = especialidade.lower().strip()

    try:
        data_hora = datetime.strptime(horario, FORMATO_DATA)
    except ValueError:
        return "Não entendi o horário. Use o formato AAAA-MM-DD HH:MM."

    with get_session() as session:
        stmt = (
            select(Horario)
            .join(Medico)
            .where(
                Medico.especialidade == especialidade,
                Horario.data_hora == data_hora,
                Horario.disponivel.is_(True),
            )
        )
        slot = session.scalars(stmt).first()

        if not slot:
            return f"Esse horário não está mais disponível para {especialidade}."

        slot.disponivel = False
        session.add(Consulta(horario_id=slot.id, nome_paciente=nome_paciente))
        session.commit()

        return f"Consulta marcada: {nome_paciente}, {especialidade}, {horario}."


@tool
def cancelar_consulta(nome_paciente: str, horario: str) -> str:
    """Cancela uma consulta já marcada, devolvendo o horário pra agenda.

    Args:
        nome_paciente: nome do paciente.
        horario: horário da consulta a ser cancelada, no formato AAAA-MM-DD HH:MM.
    """
    try:
        data_hora = datetime.strptime(horario, FORMATO_DATA)
    except ValueError:
        return "Não entendi o horário. Use o formato AAAA-MM-DD HH:MM."

    with get_session() as session:
        stmt = (
            select(Consulta)
            .join(Horario)
            .where(Consulta.nome_paciente == nome_paciente, Horario.data_hora == data_hora)
        )
        consulta = session.scalars(stmt).first()

        if not consulta:
            return "Não encontrei essa consulta pra cancelar."

        consulta.horario.disponivel = True
        session.delete(consulta)
        session.commit()

        return f"Consulta de {nome_paciente} em {horario} cancelada."


TOOLS = [consultar_agenda, marcar_consulta, cancelar_consulta]