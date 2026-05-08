# pytest tests/test_fluxo.py::test_fluxo_completo -v

from datetime import datetime, timezone, timedelta
from uuid import uuid4

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.models.token_blocklist import TokenBlocklist
from src.database.session import get_db

from pydantic import BaseModel


security = HTTPBearer()

# issuer da aplicação (quem emite o token)
ISSUER = "sistema-bancario"
AUDIENCE = "sistema-bancario-users"


class TokenPayload(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: int
    iat: int
    nbf: int
    jti: str

def sign_jwt(user_id: str) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "iss": ISSUER,
        "sub": str(user_id),
        "aud": AUDIENCE,
        "exp": int((now + timedelta(minutes=settings.access_token_expire_minutes)).timestamp()),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "jti": str(uuid4()),
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

def decode_jwt(token: str) -> TokenPayload | None:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            audience=AUDIENCE
        )

        # # verifica se token foi invalidado via logout (jti na blocklist)
        # if await is_token_blacklisted(db, payload.get("jti")):
        if payload.get("iss") != ISSUER:
            return None

        # valida estrutura via Pydantic
        return TokenPayload.model_validate(payload)

    except JWTError:
        return None
    except Exception as e:
        raise e

async def get_current_user(
    credentials=Depends(security),
    db: AsyncSession = Depends(get_db)
):
    payload = decode_jwt(credentials.credentials)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

    if await is_token_blacklisted(db, payload.jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido (logout realizado)"
        )

    return int(payload.sub)

async def is_token_blacklisted(db: AsyncSession, jti: str) -> bool:
    result = await db.execute(
        select(TokenBlocklist.jti).where(TokenBlocklist.jti == jti)
    )

    return result.scalar() is not None