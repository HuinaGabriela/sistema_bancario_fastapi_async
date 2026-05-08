from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from decimal import Decimal
from enum import Enum


class DepositoIn(BaseModel):
    valor: Decimal = Field(..., gt=0)


class SaqueIn(BaseModel):
    valor: Decimal = Field(..., gt=0)


class TipoTransacao(str, Enum):
    deposito = "deposito"
    saque = "saque"


class TransacaoOut(BaseModel):
    tipo: TipoTransacao
    valor: Decimal
    data: datetime

    class Config:
        from_attributes = True


class ExtratoOut(BaseModel):
    saldo: Decimal
    transacoes: List[TransacaoOut]

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: f"{v:.2f}"
        }