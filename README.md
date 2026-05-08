# 🏦 Sistema Bancário Async com FastAPI

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

API bancária RESTful desenvolvida com foco em:

* arquitetura em camadas
* programação assíncrona
* autenticação JWT
* testes automatizados
* boas práticas backend

---

# 🚀 Funcionalidades

* ✔ Cadastro de usuários
* ✔ Criação de contas bancárias
* ✔ Login com JWT
* ✔ Logout com blacklist de tokens
* ✔ Depósito
* ✔ Saque com validação de saldo
* ✔ Consulta de extrato
* ✔ Paginação no extrato
* ✔ Migrations com Alembic
* ✔ Ambientes isolados (dev/test/prod)

---

# 🧰 Tecnologias

* FastAPI
* SQLAlchemy Async
* SQLite
* Alembic
* Pydantic
* JWT
* Pytest
* Robot Framework
* Poetry

---

# 📁 Estrutura do Projeto

```text
src/
├── controllers/      # Endpoints da API
├── services/         # Regras de negócio
├── repositories/     # Acesso ao banco
├── models/           # Models ORM
├── schemas/          # Validações Pydantic
├── security/         # JWT e senha
├── core/             # Configurações e exceções
├── database/         # Sessão e conexão
├── utils/            # Utilitários de teste
└── main.py           # Inicialização da aplicação

alembic/              # Migrations

tests/
├── unit/             # Testes unitários
├── integration/      # Testes de integração
└── e2e/              # Testes E2E com Robot Framework
```

---

# ⚙️ Configuração do Ambiente

## Instalar dependências

```bash
poetry install
```

---

## Variáveis de ambiente

### `.env`

```env
ENVIRONMENT=dev
SECRET_KEY=abc123
```

### `.env.test`

```env
ENVIRONMENT=test
SECRET_KEY=abc123
```

---

# 🛠️ Executando o Projeto

## Aplicar migrations

```bash
poetry run alembic upgrade head
```

## Subir servidor

```bash
poetry run uvicorn src.main:app --reload
```

---

# 📌 Documentação Swagger

Após iniciar a API:

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Autenticação

A API utiliza autenticação JWT.

Fluxo:

1. Login
2. Recebimento do token
3. Envio no header:

```text
Authorization: Bearer TOKEN
```

Logout invalida o token via blocklist.

---

# 🧪 Testes

## Unit (`tests/unit`)

Testam regras de negócio isoladamente usando mocks.

```bash
pytest tests/unit -v
```

---

## Integration (`tests/integration`)

Validam integração entre API, banco e serviços.

```bash
pytest tests/integration -v
```

---

## E2E (`tests/e2e`)

Testes ponta a ponta usando Robot Framework.

```bash
.\run_robot_tests.bat
```

O script:

* sobe a API
* executa os testes
* encerra o servidor automaticamente

---

# 🔄 Alembic

## Criar migration

```bash
poetry run alembic revision --autogenerate -m "descricao"
```

## Aplicar migrations

```bash
poetry run alembic upgrade head
```

---

# 🧠 Arquitetura

O projeto utiliza separação em camadas:

```text
Controller → Service → Repository → Database
```

## Controllers

Responsáveis pelas rotas HTTP.

## Services

Contêm regras de negócio.

## Repositories

Camada de acesso ao banco.

## Schemas

Validação e serialização com Pydantic.

---

# 🔒 Segurança

* JWT com expiração
* Validação de issuer/audience
* Blocklist para logout
* Hash de senha com bcrypt
* Validações de regras de negócio

---

# ✅ Cobertura de Testes

Os testes cobrem:

* autenticação
* criação de conta
* depósitos
* saques
* extrato
* cenários inválidos
* fluxo bancário completo

---

# 🔧 Melhorias Futuras

* [ ] Docker
* [ ] PostgreSQL
* [ ] Refresh Token
* [ ] CI/CD
* [ ] Testes de concorrência
* [ ] Rate limiting

---

# 👩‍💻 Autor

Projeto desenvolvido para estudo de:

* FastAPI
* arquitetura backend
* APIs assíncronas
* testes automatizados
* boas práticas de desenvolvimento
