*** Settings ***
Resource    api_keywords.resource
Library     Collections

Resource    resources/business/auth.resource


*** Variables ***
${HEADERS}    None


*** Keywords ***

# =========================
# SETUP
# =========================

Configurar Ambiente de Teste
    Criar Sessão
    Resetar Banco
    Criar Cliente e Conta


Limpar Dados de Teste
    Resetar Banco


# =========================
# AUTH
# =========================

Autenticar Utilizador
    [Arguments]    ${cpf}    ${senha}

    ${body}=    Create Dictionary
    ...    cpf=${cpf}
    ...    senha=${senha}

    ${resp}=    POST Endpoint
    ...    /auth/login
    ...    ${body}
    ...    {}
    ...    200

    ${token}=    Set Variable    ${resp.json()["access_token"]}
    ${headers}=  Create Dictionary    Authorization=Bearer ${token}

    Set Global Variable    ${HEADERS}    ${headers}


# =========================
# SETUP DATA
# =========================

Resetar Banco
    POST Endpoint    /test/reset    {}    {}    200


Criar Cliente e Conta
    ${user}=    Create Dictionary
    ...    nome=Teste
    ...    cpf=12345678900
    ...    senha=123456
    ...    data_nascimento=2000-01-01
    ...    endereco=Rua Teste

    POST Endpoint    /accounts/users    ${user}    {}    201

    ${account}=    Create Dictionary    cpf=12345678900
    POST Endpoint    /accounts    ${account}    {}    201


# =========================
# TRANSAÇÕES
# =========================

Realizar Depósito
    [Arguments]    ${valor}

    ${body}=    Create Dictionary    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/deposit
    ...    ${body}
    ...    ${HEADERS}
    ...    200

    RETURN    ${resp.json()["saldo"]}


Realizar Saque
    [Arguments]    ${valor}

    ${body}=    Create Dictionary    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/withdraw
    ...    ${body}
    ...    ${HEADERS}
    ...    200

    RETURN    ${resp.json()["saldo"]}


Obter Extrato
    ${resp}=    GET Endpoint
    ...    /transactions/statement
    ...    ${HEADERS}
    ...    200

    RETURN    ${resp.json()}


# =========================
# CENÁRIOS DE ERRO
# =========================

Tentar Depositar
    [Arguments]    ${valor}

    ${body}=    Create Dictionary    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/deposit
    ...    ${body}
    ...    ${HEADERS}

    RETURN    ${resp}


Tentar Sacar
    [Arguments]    ${valor}

    ${body}=    Create Dictionary    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/sacar
    ...    ${body}
    ...    ${HEADERS}

    RETURN    ${resp}