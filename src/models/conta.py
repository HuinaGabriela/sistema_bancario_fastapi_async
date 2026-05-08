from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from src.database.base import Base


class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    saldo = Column(Numeric(10, 2), default=0, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), unique=False) # unique=False porque uma conta tem que ter um cliente. 

    cliente = relationship("Cliente", back_populates="contas")

    transacoes = relationship(
        "Transacao",
        back_populates="conta",
        cascade="all, delete-orphan"
    )