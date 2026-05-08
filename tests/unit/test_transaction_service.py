# pytest tests/units/test_transaction_service.py -v
import pytest
from decimal import Decimal
from unittest.mock import AsyncMock, Mock, MagicMock

from src.schemas.transaction import TipoTransacao
from src.services.account_service import AccountService
from src.services.transaction_service import TransactionService
from src.core.exceptions import BusinessError
from src.repositories.transaction_repository import TransactionRepository


class FakeConta:
    def __init__(self, id=1, saldo=0):
        self.id = id
        self.saldo = saldo

@pytest.fixture
def db():
    db = MagicMock()

    # execute precisa ser async
    db.execute = AsyncMock()

    # await db.commit() precisa ser async
    db.commit = AsyncMock()

    db.refresh = AsyncMock()

    # add é sync (SQLAlchemy session)
    db.add = MagicMock()

    return db


@pytest.fixture
def account_service():
    service = AsyncMock()

    # GARANTE que método é async
    service.obter_conta = AsyncMock()

    return service


@pytest.fixture
def service(account_service: AsyncMock, transaction_repo: AsyncMock):
    return TransactionService(account_service, transaction_repo)

@pytest.fixture
def transaction_repo():
    repo = AsyncMock()
    repo.criar = AsyncMock()
    repo.listar_por_conta = AsyncMock()
    return repo


# =========================
# SAQUE
# =========================

@pytest.mark.asyncio
async def test_saque_sem_saldo(service: TransactionService, account_service: AsyncMock):
    conta = FakeConta(saldo=Decimal("0"))
    account_service.obter_conta.return_value = conta

    with pytest.raises(BusinessError):
        await service.sacar(None, 1, Decimal("100"))


@pytest.mark.asyncio
async def test_saque_com_sucesso(service: TransactionService, account_service: AsyncMock, transaction_repo: AsyncMock, db: MagicMock):
    conta = FakeConta(saldo=Decimal("200"))
    account_service.obter_conta.return_value = conta

    await service.sacar(db, 1, Decimal("50"))

    assert conta.saldo == Decimal("150")
    # db.add.assert_called()
    transaction_repo.criar.assert_called_with(
        db,
        conta.id,
        TipoTransacao.saque,
        Decimal("50")
    )

# =========================
# DEPÓSITO
# =========================

@pytest.mark.asyncio
async def test_deposito_com_sucesso(service: TransactionService, account_service: AsyncMock, transaction_repo: AsyncMock, db: MagicMock):
    conta = FakeConta(saldo=Decimal("0"))
    account_service.obter_conta.return_value = conta

    await service.depositar(db, 1, Decimal("100"))

    assert conta.saldo == Decimal("100")
    # db.add.assert_called()
    transaction_repo.criar.assert_called_with(
        db,
        conta.id,
        TipoTransacao.deposito,
        Decimal("100")
    )

# =========================
# EXTRATO
# =========================

@pytest.mark.asyncio
async def test_extrato_retorna_saldo(service: TransactionService, account_service: AsyncMock, transaction_repo: AsyncMock, db: MagicMock):

    conta = FakeConta(saldo=Decimal("300"))
    account_service.obter_conta.return_value = conta

    # mock correto do SQLAlchemy chain
    result_mock = Mock()
    scalars_mock = Mock()

    scalars_mock.all.return_value = []
    result_mock.scalars.return_value = scalars_mock

    transaction_repo.listar_por_conta.return_value = []

    resultado = await service.extrato(db, 1, 10, 0)

    assert resultado["saldo"] == Decimal("300")


# =========================
# VALORES INVÁLIDOS
# =========================

@pytest.mark.asyncio
async def test_saque_valor_negativo(service: TransactionService, account_service: AsyncMock, db: MagicMock):
    conta = FakeConta(saldo=Decimal("100"))
    account_service.obter_conta.return_value = conta

    with pytest.raises(BusinessError):
        await service.sacar(db, 1, Decimal("-10"))

    db.add.assert_not_called()

@pytest.mark.asyncio
async def test_deposito_valor_negativo(service: TransactionService, account_service: AsyncMock, transaction_repo: AsyncMock):
    conta = FakeConta(saldo=Decimal("100"))
    account_service.obter_conta.return_value = conta

    with pytest.raises(BusinessError):
        await service.depositar(db, 1, Decimal("-50"))



# Testes: cobrir mais cenários

# ❌ saque exato (saldo == valor)
# ❌ extrato com transações reais
# ❌ múltiplos depósitos
# ❌ concorrência (avançado)