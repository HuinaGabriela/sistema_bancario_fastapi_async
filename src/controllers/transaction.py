from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.transaction_repository import TransactionRepository
from src.repositories.account_repository import AccountRepository

from src.schemas.transaction import DepositoIn, SaqueIn, ExtratoOut
from src.schemas.account import SaldoOut

from src.services.transaction_service import TransactionService
from src.services.account_service import AccountService

from src.security.jwt_service import get_current_user
from src.database.session import get_db


router = APIRouter(prefix="/transactions", tags=["Transactions"])

# dependências
account_repo = AccountRepository()
account_service = AccountService(account_repo)

transaction_repo = TransactionRepository()
transaction_service = TransactionService(account_service, transaction_repo)


@router.post("/deposit", response_model=SaldoOut)
async def depositar(
    data: DepositoIn,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    saldo = await transaction_service.depositar(db, user_id, data.valor)
    return {"saldo": saldo}


@router.post("/withdraw", response_model=SaldoOut)
async def sacar(
    data: SaqueIn,
    user_id: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    saldo = await transaction_service.sacar(db, user_id, data.valor)
    return {"saldo": saldo}


@router.get("/statement", response_model=ExtratoOut)
async def extrato(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    return await transaction_service.extrato(db, user_id, limit, skip)