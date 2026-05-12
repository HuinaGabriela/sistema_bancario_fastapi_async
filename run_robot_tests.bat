@echo off

echo =================================
echo TESTES E2E (ROBOT)
echo =================================

echo Matando processos na porta 8000...
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8000') DO (
taskkill /PID %%P /F >nul 2>&1
)

echo Subindo API...
start /B uvicorn src.main:app --host 127.0.0.1 --port 8000

echo Aguardando API subir...
timeout /t 5 /nobreak >nul

echo Rodando Robot...
robot tests/e2e

echo Finalizando API...
FOR /F "tokens=5" %%P IN ('netstat -ano ^| findstr :8000') DO (
taskkill /PID %%P /F >nul 2>&1
)

echo =================================
echo FINALIZADO
echo =================================

pause
