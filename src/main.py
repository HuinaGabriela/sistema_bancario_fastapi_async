from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from src.controllers import account, transaction, auth
from src.database.session import engine
from src.database.base import Base
from src.core.config import settings
from src.core.exceptions import BusinessError, NotFoundError
from src.utils.test_utils import router as test_router

import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App iniciando... banco deve estar migrado via Alembic")
    yield


app = FastAPI(
    title="API Bancária com SQLAlchemy",
    lifespan=lifespan
)

# Routers principais
app.include_router(auth.router)
app.include_router(account.router)
app.include_router(transaction.router)
# app.include_router(client.router)
app.include_router(test_router)

# SOMENTE EM TESTE
# if settings.environment != "prod":
#     app.include_router(test_router)


# Exception handlers globais
@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )