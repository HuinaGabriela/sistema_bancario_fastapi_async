*** Settings ***
Library    RequestsLibrary

*** Variables ***
${BASE_URL}    http://localhost:8000

*** Keywords ***

Criar Sessão
    Create Session    api    ${BASE_URL}


POST Endpoint
    [Arguments]
    ...    ${endpoint}
    ...    ${body}=${None}
    ...    ${headers}=${None}
    ...    ${expected_status}=any

    ${resp}=    POST On Session
    ...    api
    ...    ${endpoint}
    ...    json=${body}
    ...    headers=${headers}
    ...    expected_status=${expected_status}

    RETURN    ${resp}


GET Endpoint
    [Arguments]
    ...    ${endpoint}
    ...    ${headers}=${None}
    ...    ${expected_status}=any

    ${resp}=    GET On Session
    ...    api
    ...    ${endpoint}
    ...    headers=${headers}
    ...    expected_status=${expected_status}

    RETURN    ${resp}