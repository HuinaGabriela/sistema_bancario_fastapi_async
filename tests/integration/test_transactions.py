# pytest tests/integration/test_transactions.py::test_fluxo_basico -v

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from src.main import app
# from src.database.session import SessionLocal, get_db
from src.security.password import hash_password


# =========================
# OVERRIDE
# =========================
# app.dependency_overrides[get_db] = get_db


# =========================
# LIMPA BANCO
# =========================
# @pytest_asyncio.fixture(autouse=True)
# async def clean_db():
#     async with SessionLocal() as db:
#         await db.execute(text("DELETE FROM transacoes"))
#         await db.execute(text("DELETE FROM contas"))
#         await db.execute(text("DELETE FROM clientes"))
#         await db.commit()


# =========================
# SEED USUÁRIO + CONTA
# =========================
@pytest_asyncio.fixture(autouse=True)
async def seed_user(db):

        senha_hash = hash_password("123456")

        result = await db.execute(text("""
            INSERT INTO clientes (
                nome,
                cpf,
                senha_hash,
                data_nascimento,
                endereco
            )
            VALUES (
                :nome,
                :cpf,
                :senha,
                :data,
                :endereco
            )
            RETURNING id
        """), {
            "nome": "Teste Huina",
            "cpf": "12345678900",
            "senha": senha_hash,
            "data": "2000-01-01",
            "endereco": "Rua Teste"
        })

        cliente_id = result.scalar()

        # CRIA CONTA (ESSENCIAL)
        await db.execute(text("""
            INSERT INTO contas (saldo, cliente_id)
            VALUES (0, :cliente_id)
        """), {"cliente_id": cliente_id})

        await db.commit()


# =========================
# TESTE
# =========================
@pytest.mark.asyncio
async def test_fluxo_basico(client: AsyncClient):
    transport = ASGITransport(app=app)

    # async with AsyncClient(
    #     transport=transport,
    #     base_url="http://test"
    # ) as client:

    # LOGIN
    response = await client.post("/auth/login", json={
        "cpf": "12345678900",
        "senha": "123456"
    })

    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # DEPÓSITO
    response = await client.post(
        "/transactions/deposit",
        json={"valor": 100},
        headers=headers
    )
    assert response.status_code == 200

    # SAQUE
    response = await client.post(
        "/transactions/withdraw",
        json={"valor": 50},
        headers=headers
    )
    assert response.status_code == 200

    # EXTRATO
    response = await client.get(
        "/transactions/statement",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["saldo"] == "50.00"