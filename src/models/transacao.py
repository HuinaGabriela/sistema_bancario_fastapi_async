from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from src.schemas.transaction import TipoTransacao
from src.database.base import Base
from sqlalchemy import Enum


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True)
    tipo = Column(Enum(TipoTransacao), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)
    conta = relationship("Conta", back_populates="transacoes")
