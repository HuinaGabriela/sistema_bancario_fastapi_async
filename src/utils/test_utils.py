import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database.session import get_db
from src.core.config import settings


router = APIRouter(
    prefix="/test",
    tags=["Test"],
    include_in_schema=False
)

# endpoint usado apenas em testes automatizados
# impede reset fora do ambiente de testes
@router.post("/reset")
async def reset_db(db: AsyncSession = Depends(get_db)):

    # bloqueia execução fora do ambiente de testes
    if settings.environment != "test":
        raise HTTPException(
            status_code=403,
            detail="RESET só pode ser usado em ambiente de TEST"
        )

    await db.execute(text("DELETE FROM transacoes"))
    await db.execute(text("DELETE FROM contas"))
    await db.execute(text("DELETE FROM clientes"))
    await db.commit()

    return {"message": "Database resetada"}