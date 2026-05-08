from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from src.database.base import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    endereco = Column(String, nullable=False)

    contas = relationship(
        "Conta",
        back_populates="cliente",
        cascade="all, delete-orphan")