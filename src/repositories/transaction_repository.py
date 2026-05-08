from sqlalchemy import select
from src.models.transacao import Transacao


class TransactionRepository:

    async def criar(self, db, conta_id, tipo, valor):
        transacao = Transacao(
            conta_id=conta_id,
            tipo=tipo,
            valor=valor
        )
        try:
            db.add(transacao)
            await db.commit()
            await db.refresh(transacao)
            return transacao
        except Exception:
            await db.rollback()
            raise

    async def listar_por_conta(self, db, conta_id, limit, skip):
        result = await db.execute(
            select(Transacao)
            .where(Transacao.conta_id == conta_id)
            .order_by(Transacao.data.desc())
            .limit(limit)
            .offset(skip)
        )
        return result.scalars().all()