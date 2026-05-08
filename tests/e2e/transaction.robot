*** Settings ***
Resource    resources/common.resource
Resource    resources/business/auth.resource
Resource    resources/business/account.resource
Resource    resources/business/transaction.resource

Suite Setup       Configurar Ambiente de Teste
Suite Teardown    Limpar Dados de Teste

*** Test Cases ***

Cenário: Depósito com sucesso
    [Documentation]    Deve permitir depósito válido e atualizar saldo.
    [Tags]    positivo    deposito

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    ${saldo}=    Realizar Depósito    100

    Should Be Equal As Numbers    ${saldo}    100.00


Cenário: Depósito com valor negativo
    [Documentation]    Deve bloquear depósito negativo.
    [Tags]    negativo    deposito

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    ${resp}=    Tentar Depositar    -50

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    422


Cenário: Depósito com valor zero
    [Documentation]    Deve bloquear depósito com valor zero.
    [Tags]    negativo    deposito

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    ${resp}=    Tentar Depositar    0

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    422


# =========================
# SAQUE
# =========================

Cenário: Saque com sucesso
    [Documentation]    Deve permitir saque com saldo suficiente.
    [Tags]    positivo    saque

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    Realizar Depósito    100
    ${saldo}=    Realizar Saque    50

    Should Be Equal As Numbers    ${saldo}    50.00


Cenário: Saque com saldo insuficiente
    [Documentation]    Deve bloquear saque maior que saldo.
    [Tags]    negativo    saque

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    Realizar Depósito    50
    ${resp}=    Tentar Sacar    100

    Should Be Equal As Integers    ${resp.status_code}    404


Cenário: Saque com valor exato
    [Documentation]    Deve permitir sacar todo o saldo.
    [Tags]    positivo    saque

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    Realizar Depósito    100
    ${saldo}=    Realizar Saque    100

    Should Be Equal As Numbers    ${saldo}    0.00


# =========================
# EXTRATO
# =========================

Cenário: Extrato sem transações
    [Documentation]    Deve retornar saldo zero e lista vazia.
    [Tags]    extrato

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    ${extrato}=    Obter Extrato

    Should Be Equal As Numbers    ${extrato["saldo"]}    0.00
    Length Should Be    ${extrato["transacoes"]}    0


Cenário: Extrato com múltiplas transações
    [Documentation]    Deve retornar transações em ordem correta.
    [Tags]    extrato

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    Realizar Depósito    100
    Realizar Saque       30
    Realizar Depósito    20

    ${extrato}=    Obter Extrato

    Should Be Equal As Numbers    ${extrato["saldo"]}    90.00

    # valida ordem: mais recente primeiro
    ${transacoes}=    Set Variable    ${extrato["transacoes"]}

    Should Be Equal    ${transacoes[0]["tipo"]}    deposito
    Should Be Equal    ${transacoes[1]["tipo"]}    saque
    Should Be Equal    ${transacoes[2]["tipo"]}    deposito


# =========================
# TOKEN
# =========================

Cenário: Acesso sem token
    [Documentation]    Deve bloquear acesso sem autenticação.
    [Tags]    auth

    ${resp}=    Tentar Depositar Sem Token    100

    Should Be Equal As Integers    ${resp.status_code}    401


Cenário: Token inválido
    [Documentation]    Deve bloquear token inválido.
    [Tags]    auth

    ${resp}=    Tentar Depositar Com Token Invalido    100

    Should Be Equal As Integers    ${resp.status_code}    401