# Estratégia de Testes

O projeto utiliza uma arquitetura de testes baseada na pirâmide de testes, separando responsabilidades entre testes unitários, integração e ponta a ponta (E2E).

## Estrutura

```text
tests/
├── unit/
│   └── test_transaction_service.py
│
├── integration/
│   ├── test_auth.py
│   ├── test_transactions.py
│   └── test_fluxo.py
│
└── e2e/
    ├── account.robot
    ├── auth.robot
    ├── transaction.robot
    └── fluxo_bancario.robot



## Unit (`tests/unit`)

Testam regras de negócio isoladas utilizando mocks.

Características:

rápidos
independentes de banco/API
utilizam mocks (AsyncMock, MagicMock)
focados em services

Exemplos:

depósito
saque
validações
saldo insuficiente
extrato

Executar:
pytest tests/unit -v




## Integration (`tests/integration`)

Validam integração real entre:

rotas FastAPI
autenticação JWT
banco de dados
repositories
services

Características:

utilizam AsyncClient
executam chamadas HTTP reais
validam fluxo backend completo
mais lentos que unitários

Exemplos:

login
logout
depósito
saque
extrato
fluxo completo autenticado

Executar:
pytest tests/integration -v




## E2E (`tests/e2e`)

Validam comportamento do sistema do ponto de vista do usuário.

Utilizam:

Robot Framework
RequestsLibrary

Características:

simulam uso real da API
validam comportamento ponta a ponta
possuem maior custo de execução
geram relatórios HTML

Exemplos:

autenticação
criação de conta
depósitos
saques
extrato
fluxo bancário completo

Executar:
run_robot_tests.bat
ou
robot tests/e2e

Após execução são gerados:

log.html → execução detalhada
report.html → resumo dos testes
output.xml → resultado bruto

Organização dos Resources (Robot)

Os testes Robot utilizam arquivos .resource para reutilização de keywords.

Estrutura:
resources/
├── api/
│   └── api_keywords.resource
│
├── business/
│   ├── account.resource
│   ├── auth.resource
│   └── transaction.resource
│
└── common.resource


| Arquivo                 | Responsabilidade              |
| ----------------------- | ----------------------------- |
| `api_keywords.resource` | comunicação HTTP              |
| `account.resource`      | operações de conta            |
| `auth.resource`         | autenticação                  |
| `transaction.resource`  | transações                    |
| `common.resource`       | setup, teardown e utilitários |


Boas práticas adotadas:
separação por camada de teste
uso de fixtures
isolamento de responsabilidades
keywords reutilizáveis
geração de CPF dinâmico
testes positivos e negativos
validação de autenticação/autorização
relatórios HTML para E2E


pip install pytest pytest-asyncio httpx
pip install robotframework
