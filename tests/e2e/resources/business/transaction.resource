*** Settings ***
Resource    ../api/api_keywords.resource


*** Keywords ***

Realizar Depósito
    [Arguments]    ${valor}

    ${body}=    Create Dictionary
    ...    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/deposit
    ...    ${body}
    ...    ${HEADERS}

    Should Be Equal As Integers    ${resp.status_code}    200

    RETURN    ${resp.json()["saldo"]}


Tentar Depositar
    [Arguments]    ${valor}

    ${body}=    Create Dictionary    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/deposit
    ...    ${body}
    ...    ${HEADERS}
    ...    expected_status=any

    RETURN    ${resp}


Tentar Sacar
    [Arguments]    ${valor}

    ${body}=    Create Dictionary    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/sacar
    ...    ${body}
    ...    ${HEADERS}
    ...    expected_status=any

    RETURN    ${resp}


Realizar Saque
    [Arguments]    ${valor}

    ${body}=    Create Dictionary
    ...    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/withdraw
    ...    ${body}
    ...    ${HEADERS}

    Should Be Equal As Integers    ${resp.status_code}    200

    RETURN    ${resp.json()["saldo"]}


Consultar Extrato

    ${resp}=    GET Endpoint
    ...    /transactions/statement
    ...    ${HEADERS}

    Should Be Equal As Integers    ${resp.status_code}    200

    RETURN    ${resp.json()}


Obter Extrato

    ${resp}=    GET Endpoint
    ...    /transactions/statement
    ...    ${HEADERS}

    Should Be Equal As Integers    ${resp.status_code}    200

    RETURN    ${resp.json()}


Tentar Depositar Sem Token
    [Arguments]    ${valor}

    ${body}=    Create Dictionary
    ...    valor=${valor}

    ${resp}=    POST Endpoint
    ...    /transactions/deposit
    ...    ${body}
    ...    expected_status=any

    RETURN    ${resp}


Tentar Depositar Com Token Invalido
    [Arguments]    ${valor}

    ${body}=    Create Dictionary
    ...    valor=${valor}

    ${headers}=    Create Dictionary
    ...    Authorization=Bearer token_fake

    ${resp}=    POST Endpoint
    ...    /transactions/deposit
    ...    ${body}
    ...    ${headers}
    ...    expected_status=any

    RETURN    ${resp}
