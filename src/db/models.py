from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Medico(Base):
    __tablename__ = "medicos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    especialidade: Mapped[str] = mapped_column(String(80), index=True)

    horarios: Mapped[list["Horario"]] = relationship(back_populates="medico")

class Horario(Base):
    __tablename__ = "horarios"
 
    id: Mapped[int] = mapped_column(primary_key=True)
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id"))
    data_hora: Mapped[datetime] = mapped_column(DateTime)
    disponivel: Mapped[bool] = mapped_column(Boolean, default=True)
 
    medico: Mapped["Medico"] = relationship(back_populates="horarios")
    consulta: Mapped["Consulta"] = relationship(back_populates="horario", uselist=False)
 
class Consulta(Base):
    __tablename__ = "consultas"
 
    id: Mapped[int] = mapped_column(primary_key=True)
    horario_id: Mapped[int] = mapped_column(ForeignKey("horarios.id"), unique=True)
    nome_paciente: Mapped[str] = mapped_column(String(120))
    criada_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
 
    horario: Mapped["Horario"] = relationship(back_populates="consulta")
