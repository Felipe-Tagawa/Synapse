"""
Conexão com o Postgres. A URL vem de uma variável de ambiente pra não
deixar credencial hardcoded no código.

Formato esperado do DATABASE_URL:
postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não configurada. Crie um arquivo .env na raiz do "
        "projeto com: DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/banco"
    )

engine = create_engine(DATABASE_URL)


def criar_tabelas():
    Base.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)