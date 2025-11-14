# 13ft Ladder Server Launcher
# This script activates the virtual environment and starts the Flask server

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  13ft Ladder - Paywall Bypass Server" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Get the script's directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to the 13ft directory
Set-Location $ScriptDir

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run the installation first." -ForegroundColor Yellow
    pause
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Start the server
Write-Host ""
Write-Host "Starting 13ft server on http://127.0.0.1:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Wait a moment for Flask to start
Start-Sleep -Seconds 2

# Open browser
Start-Process "http://127.0.0.1:5000"

# Run the Flask app
python app\portable.py
