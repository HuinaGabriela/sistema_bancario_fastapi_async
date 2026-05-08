*** Settings ***
Resource    resources/common.resource
Resource    resources/business/auth.resource
Resource    resources/business/account.resource
Resource    resources/business/transaction.resource

Suite Setup       Configurar Ambiente de Teste
Suite Teardown    Limpar Dados de Teste

*** Test Cases ***

Fluxo Bancário Completo
    [Tags]    regressao

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}

    Autenticar Utilizador    ${cpf}    123456

    ${saldo}=    Realizar Depósito    100
    Should Be Equal As Numbers    ${saldo}    100.00

    ${saldo}=    Realizar Saque    50
    Should Be Equal As Numbers    ${saldo}    50.00

    ${extrato}=    Consultar Extrato

    Should Be Equal As Numbers
    ...    ${extrato["saldo"]}
    ...    50.00