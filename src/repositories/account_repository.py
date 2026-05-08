from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.models.cliente import Cliente
from src.models.conta import Conta


class AccountRepository:

    # =====================
    # CLIENTE
    # =====================

    async def buscar_cliente_por_cpf(self, db, cpf: str):
        result = await db.execute(
            select(Cliente).where(Cliente.cpf == cpf)
        )
        return result.scalars().first()

    async def criar_cliente(self, db, cliente: Cliente):
        try:
            db.add(cliente)
            await db.commit()
            await db.refresh(cliente)
            return cliente
        except IntegrityError:
            await db.rollback()
            raise

    # =====================
    # CONTA
    # =====================

    async def buscar_conta_por_cliente_id(self, db, cliente_id: int):
        result = await db.execute(
            select(Conta).where(Conta.cliente_id == cliente_id)
        )
        return result.scalars().first()

    async def criar_conta(self, db, conta: Conta):
        try:
            db.add(conta)
            await db.commit()
            await db.refresh(conta)
            return conta
        except IntegrityError:
            await db.rollback()
            raise