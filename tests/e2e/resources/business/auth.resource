*** Settings ***
Resource    ../api/api_keywords.resource

*** Keywords ***

Fazer Login
    [Arguments]    ${cpf}    ${senha}

    ${body}=    Create Dictionary
    ...    cpf=${cpf}
    ...    senha=${senha}

    ${resp}=    POST Endpoint
    ...    /auth/login
    ...    ${body}

    RETURN    ${resp}


Autenticar Utilizador
    [Arguments]    ${cpf}    ${senha}

    ${resp}=    Fazer Login
    ...    ${cpf}
    ...    ${senha}

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    200

    ${token}=    Set Variable
    ...    ${resp.json()["access_token"]}

    ${headers}=    Create Dictionary
    ...    Authorization=Bearer ${token}

    Set Suite Variable
    ...    ${HEADERS}
    ...    ${headers}


Tentar Login
    [Arguments]    ${cpf}    ${senha}

    ${body}=    Create Dictionary
    ...    cpf=${cpf}
    ...    senha=${senha}

    ${resp}=    POST Endpoint
    ...    /auth/login
    ...    ${body}
    ...    expected_status=any

    RETURN    ${resp}