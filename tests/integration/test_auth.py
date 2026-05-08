# pytest tests/integration/test_auth.py::test_logout_invalida_token -v
import pytest


@pytest.mark.asyncio
async def test_logout_invalida_token(client):
    # 1. criar usuário
    await client.post("/accounts/users", json={
        "nome": "João",
        "cpf": "12345678900",
        "senha": "123456",
        "data_nascimento": "2000-01-01",
        "endereco": "Rua A"
    })

    # 2. criar conta
    await client.post("/accounts/", json={
        "cpf": "12345678900"
    })

    # 3. login
    response = await client.post("/auth/login", json={
        "cpf": "12345678900",
        "senha": "123456"
    })

    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. logout
    response = await client.post("/auth/logout", headers=headers)
    assert response.status_code == 200

    # 5. tenta usar token novamente
    response = await client.post(
        "/transactions/deposit",
        json={"valor": 100},
        headers=headers
    )

    assert response.status_code == 401