@echo off
TITLE Explorador de Indices Climaticos - Web Server

echo =======================================================
echo   Explorador Interativo de Indices Climaticos
echo   Servidor Web Local
echo =======================================================
echo.

set PYTHON_CMD=python

where C:\Users\haas\miniforge3\python.exe >nul 2>nul
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=C:\Users\haas\miniforge3\python.exe
    goto RUN_SERVER
)

where python >nul 2>nul
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=python
    goto RUN_SERVER
)

where py >nul 2>nul
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=py
    goto RUN_SERVER
)

echo ERROR: Python nao foi encontrado no sistema. Por favor instale o Python.
pause
exit /b 1

:RUN_SERVER
echo Iniciando o servidor web na porta 8080...
echo.
"%PYTHON_CMD%" serve_app.py

pause
