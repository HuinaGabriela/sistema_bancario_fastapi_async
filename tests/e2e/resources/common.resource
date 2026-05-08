*** Settings ***
Resource    api/api_keywords.resource

*** Keywords ***

Configurar Ambiente de Teste
    Criar Sessão
    POST Endpoint    /test/reset


Limpar Dados de Teste
    POST Endpoint    /test/reset


Gerar CPF Dinâmico
    ${cpf}=    Evaluate    str(random.randint(10000000000,99999999999))    random
    RETURN    ${cpf}