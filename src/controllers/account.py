from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.account import CreateUser, CreateAccount,  UserOut, AccountOut
from src.services.account_service import AccountService
from src.database.session import get_db
from src.core.exceptions import BusinessError, NotFoundError
from src.repositories.account_repository import AccountRepository


router = APIRouter(prefix="/accounts", tags=["Accounts"])

account_repo = AccountRepository()
service = AccountService(account_repo)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def criar_usuario(data: CreateUser, db: AsyncSession = Depends(get_db)):
    try:
        return await service.criar_usuario(db, data)
    except BusinessError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
async def criar_conta(data: CreateAccount, db: AsyncSession = Depends(get_db)):
    try:
        return await service.criar_conta(db, data.cpf)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))