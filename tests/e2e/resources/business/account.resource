*** Settings ***
Resource    ../api/api_keywords.resource
Library     Collections

*** Keywords ***

Criar Usuário
    [Arguments]    ${cpf}

    ${user}=    Create Dictionary
    ...    nome=Teste
    ...    cpf=${cpf}
    ...    senha=123456
    ...    data_nascimento=2000-01-01
    ...    endereco=Rua Teste

    ${resp}=    POST Endpoint
    ...    /accounts/users
    ...    ${user}

    RETURN    ${resp}


Criar Conta
    [Arguments]    ${cpf}

    ${account}=    Create Dictionary
    ...    cpf=${cpf}

    ${resp}=    POST Endpoint
    ...    /accounts
    ...    ${account}

    RETURN    ${resp}


Criar Cliente e Conta
    [Arguments]    ${cpf}

    ${resp}=    Criar Usuário    ${cpf}

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    201

    ${resp}=    Criar Conta    ${cpf}

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    201


Tentar Criar Usuário Duplicado
    [Arguments]    ${cpf}

    ${user}=    Create Dictionary
    ...    nome=Teste
    ...    cpf=${cpf}
    ...    senha=123456
    ...    data_nascimento=2000-01-01
    ...    endereco=Rua Teste

    ${resp}=    POST Endpoint
    ...    /accounts/users
    ...    ${user}
    ...    ${None}
    ...    any

    RETURN    ${resp}


Tentar Criar Conta
    [Arguments]    ${cpf}

    ${account}=    Create Dictionary
    ...    cpf=${cpf}

    ${resp}=    POST Endpoint
    ...    /accounts
    ...    ${account}
    ...    ${None}
    ...    any

    RETURN    ${resp}

