@echo off
REM 13ft Ladder Server Launcher (Batch version)
REM This script activates the virtual environment and starts the Flask server

echo ================================================
echo   13ft Ladder - Paywall Bypass Server
echo ================================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run the installation first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Start the server
echo.
echo Starting 13ft server on http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

REM Open browser after a short delay
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5000

REM Run the Flask app
python app\portable.py

pause
