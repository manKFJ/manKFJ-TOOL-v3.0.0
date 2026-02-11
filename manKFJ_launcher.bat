@echo off
chcp 65001 >nul
title manKFJ Security Tool v3.0.0
color 0A

echo.
echo ========================================
echo     manKFJ Security Tool v3.0.0
echo     Penetration Testing Framework
echo ========================================
echo.

:: Check Python
python --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python non trovato!
    echo Installa Python 3 da: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

:: Check if script exists
if not exist "manKFJ_tool.py" (
    echo [ERROR] File manKFJ_tool.py non trovato!
    echo Assicurati che sia nella stessa cartella.
    echo.
    pause
    exit /b 1
)

:menu
cls
echo.
echo ========================================
echo          manKFJ MAIN MENU
echo ========================================
echo [1] Esegui manKFJ Security Tool
echo [2] Installa dipendenze
echo [3] Informazioni
echo [4] Esci
echo ========================================
echo.

set /p choice="[manKFJ] > "

if "%choice%"=="1" goto run
if "%choice%"=="2" goto install
if "%choice%"=="3" goto info
if "%choice%"=="4" goto exit
goto menu

:run
echo.
echo [*] Avvio manKFJ Security Tool...
echo.
python manKFJ_tool.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Si e verificato un errore!
)
echo.
pause
goto menu

:install
echo.
echo [*] Installazione dipendenze Python...
echo.
pip install --upgrade pip
pip install requests colorama
echo.
echo [*] Dipendenze opzionali:
echo     pip install paramiko dnspython whois
echo.
pause
goto menu

:info
cls
echo.
echo ========================================
echo        manKFJ SECURITY TOOL
echo ========================================
echo Versione: 3.0.0
echo Author: manKFJ Team
echo.
echo FUNZIONALITA:
echo - Port Scanner
echo - Vulnerability Scanner
echo - Password Cracker
echo - Web Testing
echo - DDoS Simulator (EDU)
echo - Brute Force
echo - SQL Injection Tester
echo.
echo AVVERTENZA:
echo Solo per scopi educativi!
echo Usare solo su sistemi autorizzati.
echo ========================================
echo.
pause
goto menu

:exit
echo.
echo [*] Grazie per aver usato manKFJ!
echo [*] Stay secure!
echo.
timeout /t 2 >nul
exit /b 0