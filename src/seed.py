"""
Roda uma vez pra criar as tabelas e popular o banco com dados de teste.
Uso: python seed.py
"""

from datetime import datetime

from db.database import criar_tabelas, get_session
from db.models import Horario, Medico

MEDICOS_TESTE = [
    {
        "nome": "Dra. Ana Souza",
        "especialidade": "cardiologista",
        "horarios": ["2026-09-10 09:00", "2026-09-10 14:00", "2026-09-11 10:00"],
    },
    {
        "nome": "Dr. Bruno Lima",
        "especialidade": "dermatologista",
        "horarios": ["2026-09-09 08:30", "2026-09-12 15:00"],
    },
    {
        "nome": "Dra. Carla Dias",
        "especialidade": "clinico geral",
        "horarios": ["2026-09-08 09:00", "2026-09-08 11:00", "2026-09-09 16:00"],
    },
]


def rodar_seed():
    criar_tabelas()

    with get_session() as session:
        for dados_medico in MEDICOS_TESTE:
            medico = Medico(nome=dados_medico["nome"], especialidade=dados_medico["especialidade"])
            session.add(medico)
            session.flush()  # garante o id do médico antes de criar os horários

            for horario_str in dados_medico["horarios"]:
                data_hora = datetime.strptime(horario_str, "%Y-%m-%d %H:%M")
                session.add(Horario(medico_id=medico.id, data_hora=data_hora, disponivel=True))

        session.commit()

    print("Banco populado com sucesso.")


if __name__ == "__main__":
    rodar_seed()