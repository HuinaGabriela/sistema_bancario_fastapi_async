# 🏦 Sistema Bancário Async com FastAPI

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)


API REST bancária assíncrona desenvolvida com foco em arquitetura backend moderna, autenticação JWT e testes automatizados em múltiplos níveis.

---

# 🚀 Destaques técnicos

* ✔ Arquitetura em camadas (Controller → Service → Repository)
* ✔ API assíncrona com FastAPI
* ✔ Autenticação JWT com blacklist de tokens
* ✔ Banco de dados com SQLAlchemy assíncrono + Alembic
* ✔ Testes automatizados (unitários, integração e E2E)
* ✔ Cobertura de testes (~82%)
* ✔ Ambiente separado para dev e testes

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

# 🔐 Autenticação

A API utiliza autenticação JWT.

Fluxo:
1. Login com CPF e senha
2. Geração de token JWT
3. Uso do token via header Authorization
4. Logout invalida token via blacklist

---

# ✅ Cobertura de Testes

O projeto possui testes em 3 níveis:

- Unitários: regras de negócio isoladas
  
- Integração: API + banco de dados
  
- E2E: fluxos completos com Robot Framework
  

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


📊 Test Coverage

Execução de testes de cobertura:

pytest --cov=src --cov-report=term-missing

Resultado atual:

![Coverage](https://img.shields.io/badge/coverage-82%25-green)

Total de linhas: 475

Linhas não cobertas: 87

Cobertura por camada:

| Camada       | Cobertura                  |
| ------------ | -------------------------- |
| Controllers  | Parcial (73% - 92%)        |
| Services     | ⚠️ Baixa (48% - 100%)      |
| Repositories | ⚠️ Média/baixa (59% - 62%) |
| Schemas      | Alta (95% - 100%)          |
| Models       | 100%                       |
| Core / Utils | 56% - 100%                 |

🧠 Interpretação da cobertura

A cobertura atual é considerada boa para fins de portfólio e aprendizado (82%), porém com concentração de lacunas em:

- Camada de serviços (regras de negócio)

- Camada de repositórios (acesso a dados)

- Alguns fluxos alternativos de autenticação

🚧 Melhorias planejadas (roadmap técnico)

As seguintes melhorias foram identificadas para evolução futura do projeto:

🔴 Prioridade alta

Aumentar cobertura da camada account_service

Melhorar testes de regras de negócio (validações e fluxos alternativos)

🟡 Prioridade média

Expandir testes dos repositórios (account_repository, transaction_repository)

Cobrir cenários de erro em autenticação

🟢 Prioridade baixa

Melhorar cobertura do JWT service (expiração e edge cases)

Reduzir warnings de depreciação do Pydantic e datetime

---

# 👩‍💻 Autor

Projeto desenvolvido para estudo de:

* FastAPI
* arquitetura backend
* APIs assíncronas
* testes automatizados
* boas práticas de desenvolvimento
