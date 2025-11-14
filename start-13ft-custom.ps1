# 13ft Ladder Server Launcher (Custom Port/Host)
# This script allows you to specify custom host and port

param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 5000
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  13ft Ladder - Paywall Bypass Server" -ForegroundColor Cyan
Write-Host "  Custom Configuration" -ForegroundColor Cyan
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
Write-Host "Starting 13ft server on http://${Host}:${Port}" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Set environment variables
$env:FLASK_APP = "app\portable.py"

# Wait a moment then open browser
Start-Sleep -Seconds 2
Start-Process "http://${Host}:${Port}"

# Run Flask with custom host and port
flask run --host=$Host --port=$Port --no-debugger
