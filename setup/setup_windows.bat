@echo off
SETLOCAL ENABLEEXTENSIONS

:: Check if run as Administrator
net session >nul 2>&1
if %errorlevel% == 1 (
    echo This script requires Administrator privileges.
    echo Please run this script as an Administrator.
    pause
    exit
)

:: Install NSSM if not already installed (adjust the path to nssm.exe as necessary)
if not exist "C:\Program Files\NSSM\nssm.exe" (
    echo Installing NSSM...
    powershell -command "Invoke-WebRequest -Uri 'https://nssm.cc/release/nssm-2.24.zip' -OutFile 'nssm.zip'"
    powershell -command "Expand-Archive -Path 'nssm.zip' -DestinationPath 'C:\Program Files\NSSM'"
    del nssm.zip
    echo NSSM installed.
)

:: Setting up environment variables, adjust as necessary
echo Setting up environment variables...
setx SCYTHEX_HOME "%~dp0"

:: Registering ScytheEx as a service
echo Registering ScytheEx as a Windows Service...
"C:\Program Files\NSSM\nssm.exe" install ScytheEx "python" "%SCYTHEX_HOME%main.py"
"C:\Program Files\NSSM\nssm.exe" set ScytheEx AppDirectory "%SCYTHEX_HOME%"
"C:\Program Files\NSSM\nssm.exe" set ScytheEx AppParameters ""
"C:\Program Files\NSSM\nssm.exe" set ScytheEx DisplayName "ScytheEx Network Traffic Monitor"
"C:\Program Files\NSSM\nssm.exe" set ScytheEx Start SERVICE_AUTO_START
net start ScytheEx

echo ScytheEx service has been installed and started.
echo Setup complete!
pause
