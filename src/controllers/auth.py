from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.models.token_blocklist import TokenBlocklist
from src.security.jwt_service import decode_jwt, security
from src.services.account_service import AccountService
from src.schemas.auth import LoginIn, LoginOut
from src.core.exceptions import BusinessError
from src.security.jwt_service import sign_jwt
from fastapi import status
from src.repositories.account_repository import AccountRepository

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/auth", tags=["Auth"])

account_repo = AccountRepository()
service = AccountService(account_repo)


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn, db: AsyncSession = Depends(get_db)):
    try:
        user = await service.autenticar(db, data.cpf, data.senha)

        token = sign_jwt(user.id)
        logger.info(f"Login realizado | user_id={user.id}")

        return {"access_token": token}

    except BusinessError as e:
        logger.warning(f"Login inválido | cpf={data.cpf}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/logout")
async def logout(
    credentials=Depends(security),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_jwt(credentials.credentials)

    if payload is None:
        logger.warning("Logout falhou | token inválido")

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )
    
    # salvar na blacklist
    token = TokenBlocklist(jti=payload.jti)
    db.add(token)
    await db.commit()

    logger.info(f"Logout realizado | user_id={payload.sub}")

    return {"message": "Logout realizado com sucesso"}
