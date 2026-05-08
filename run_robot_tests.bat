@echo off

echo ================================
echo TESTES E2E (ROBOT)
echo ================================

echo Matando processos na porta 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /PID %%a /F >nul 2>&1

echo Subindo API...

set ENVIRONMENT=test
set SECRET_KEY=abc123

start "" cmd /c "poetry run uvicorn src.main:app --port 8000"

echo Aguardando API subir...

:wait_loop
curl -s http://localhost:8000/docs >nul 2>&1

if errorlevel 1 (
    timeout /t 1 >nul
    goto wait_loop
)

echo Rodando Robot...

robot .\test\e2e

echo Finalizando API...

for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /PID %%a /F >nul 2>&1

echo ================================
echo FINALIZADO
echo ================================

pause