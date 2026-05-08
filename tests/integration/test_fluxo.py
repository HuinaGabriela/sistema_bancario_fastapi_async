# pytest tests/test_fluxo.py::test_fluxo_completo -v  
import pytest


@pytest.mark.asyncio
async def test_fluxo_completo(client):
    # 1. criar usuário
    response = await client.post("/accounts/users", json={
        "nome": "Gabriela",
        "cpf": "12345678900",
        "senha": "123456",
        "data_nascimento": "2000-01-01",
        "endereco": "Rua A"
    })
    assert response.status_code == 201

    # 2. criar conta
    response = await client.post("/accounts/", json={
        "cpf": "12345678900"
    })
    assert response.status_code == 201

    # 3. login
    response = await client.post("/auth/login", json={
        "cpf": "12345678900",
        "senha": "123456"
    })
    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. depósito
    response = await client.post(
        "/transactions/deposit",
        json={"valor": 100},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["saldo"] == "100.00"

    # 5. saque
    response = await client.post(
        "/transactions/withdraw",
        json={"valor": 50},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["saldo"] == "50.00"

    # 6. extrato
    response = await client.get(
        "/transactions/statement",
        headers=headers
    )
    assert response.status_code == 200

    data = response.json()

    # valida saldo final
    assert data["saldo"] == "50.00"

    # valida quantidade de transações
    assert len(data["transacoes"]) == 2

    # valida ordem (mais recente primeiro)
    assert data["transacoes"][0]["tipo"] == "saque"
    assert data["transacoes"][1]["tipo"] == "deposito"