*** Settings ***
Library    Collections
Resource    resources/common.resource
Resource    resources/business/auth.resource
Resource    resources/business/account.resource
Resource    resources/business/transaction.resource


*** Keywords ***

Configurar Ambiente de Teste
    Criar Sessão
    POST Endpoint    /test/reset    ${None}

Limpar Dados de Teste
    POST Endpoint    /test/reset    ${None}


*** Test Cases ***

Cenário: Login com sucesso
    [Documentation]    Deve autenticar utilizador válido.
    [Tags]    positivo    auth

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}
    Autenticar Utilizador    ${cpf}    123456

    ${resp}=    Fazer Login
    ...    ${cpf}
    ...    123456

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    200

    Dictionary Should Contain Key
    ...    ${resp.json()}
    ...    access_token


Cenário: Login com senha inválida
    [Documentation]    Deve bloquear login com senha incorreta.
    [Tags]    negativo    auth

    ${cpf}=    Gerar CPF Dinâmico

    Criar Cliente e Conta    ${cpf}

    ${resp}=    Tentar Login
    ...    ${cpf}
    ...    senha_errada

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    400


Cenário: Login com CPF inexistente
    [Documentation]    Deve bloquear login de utilizador inexistente.
    [Tags]    negativo    auth

    ${cpf}=    Gerar CPF Dinâmico

    ${resp}=    Tentar Login
    ...    ${cpf}
    ...    123456

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    400


Cenário: Acesso com token inválido
    [Documentation]    Deve bloquear token inválido.
    [Tags]    auth

    ${resp}=    Tentar Depositar Com Token Invalido    100

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    401


Cenário: Acesso sem token
    [Documentation]    Deve bloquear acesso sem autenticação.
    [Tags]    auth

    ${resp}=    Tentar Depositar Sem Token    100

    Should Be Equal As Integers
    ...    ${resp.status_code}
    ...    401