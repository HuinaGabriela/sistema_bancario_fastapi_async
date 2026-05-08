from pydantic import BaseModel, Field, field_validator, field_serializer
from datetime import date
import re
from decimal import Decimal


class CPFSchema(BaseModel):
    cpf: str

    @field_validator("cpf")
    def validar_cpf(cls, v):
        v = re.sub(r"\D", "", v)
        if len(v) != 11:
            raise ValueError("CPF inválido")
        return v


class CreateUser(CPFSchema):
    nome: str = Field(..., min_length=3)
    senha: str = Field(..., min_length=6)
    data_nascimento: date
    endereco: str = Field(..., min_length=5)

    @field_validator("data_nascimento")
    def validar_data_nascimento(cls, v):
        if v > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro")
        return v


class CreateAccount(CPFSchema):
    pass


class AccountOut(BaseModel):
    id: int
    saldo: Decimal
    cliente_id: int

    class Config:
        from_attributes = True
        json_encoders = {
            Decimal: lambda v: f"{v:.2f}"
        }


class UserOut(BaseModel):
    id: int
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str

    class Config:
        from_attributes = True


class SaldoOut(BaseModel):
    saldo: Decimal

    @field_serializer("saldo")
    def formatar_saldo(self, value: Decimal):
        return f"{value:.2f}"