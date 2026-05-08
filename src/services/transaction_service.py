from src.schemas.transaction import TipoTransacao
from src.core.exceptions import BusinessError
from decimal import Decimal

import logging

logger = logging.getLogger(__name__)


class TransactionService:

    def __init__(self, account_service, transaction_repo):
        self.account_service = account_service
        self.transaction_repo = transaction_repo

    async def depositar(self, db, user_id, valor):
        valor = Decimal(valor)

        if valor <= 0:
            raise BusinessError("Valor deve ser positivo")

        # async with db.begin():
        conta = await self.account_service.obter_conta(db, user_id)

        await db.refresh(conta)

        conta.saldo += valor

        await self.transaction_repo.criar(db, conta.id, TipoTransacao.deposito, valor)

        logger.info(f"Depósito realizado | user_id={user_id} valor={valor} saldo={conta.saldo}")

        return conta.saldo

    async def sacar(self, db, user_id, valor):
        valor = Decimal(valor)

        if valor <= 0:
            raise BusinessError("Valor deve ser positivo")

        # async with db.begin():
        conta = await self.account_service.obter_conta(db, user_id)

        if conta.saldo < valor:
            logger.warning(f"Saque negado | user_id={user_id} valor={valor} saldo={conta.saldo}")
            raise BusinessError("Saldo insuficiente")

        # refresh garante estado atualizado
        await db.refresh(conta)

        conta.saldo -= valor

        await self.transaction_repo.criar(db, conta.id, TipoTransacao.saque, valor)

        logger.info(f"Saque realizado | user_id={user_id} valor={valor} saldo={conta.saldo}")

        return conta.saldo

    async def extrato(self, db, user_id: int, limit: int, skip: int):
        conta = await self.account_service.obter_conta(db, user_id)

        transacoes = await self.transaction_repo.listar_por_conta(db, conta.id, limit, skip)

        logger.info(
            f"Extrato consultado | user_id={user_id} count={len(transacoes)} limit={limit} skip={skip}"
        )

        return {
            "saldo": conta.saldo,
            "transacoes": [
                {
                    "tipo": t.tipo.value,
                    "valor": t.valor,
                    "data": t.data.isoformat()
                }
                for t in transacoes
            ]
        }