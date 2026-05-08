*** Settings ***
Resource    resources/common.resource
Resource    resources/business/account.resource

Suite Setup       Configurar Ambiente de Teste
Suite Teardown    Limpar Dados de Teste


*** Test Cases ***

Cenário: Criar usuário com sucesso
    [Documentation]    Deve criar usuário válido.
    [Tags]    positivo    conta

    ${cpf}=    Gerar CPF Dinâmico

    ${resp}=    Criar Usuário
    ...    ${cpf}

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    201


Cenário: Criar usuário com CPF duplicado
    [Documentation]    Deve bloquear CPF duplicado.
    [Tags]    negativo    conta

    ${cpf}=    Gerar CPF Dinâmico

    Criar Usuário    ${cpf}

    ${resp}=    Tentar Criar Usuário Duplicado
    ...    ${cpf}

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    400


Cenário: Criar conta com sucesso
    [Documentation]    Deve criar conta para usuário válido.
    [Tags]    positivo    conta

    ${cpf}=    Gerar CPF Dinâmico

    Criar Usuário    ${cpf}

    ${resp}=    Criar Conta
    ...    ${cpf}

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    201


Cenário: Criar conta para usuário inexistente
    [Documentation]    Deve bloquear conta para CPF inexistente.
    [Tags]    negativo    conta

    ${cpf}=    Gerar CPF Dinâmico

    ${resp}=    Tentar Criar Conta
    ...    ${cpf}

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    404