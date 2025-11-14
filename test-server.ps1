# Quick test script to verify 13ft server works
Write-Host "Testing 13ft server installation..." -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Check virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment missing" -ForegroundColor Red
    exit 1
}

# Check Python packages
& "venv\Scripts\Activate.ps1"
$packages = pip list 2>$null
if ($packages -match "flask") {
    Write-Host "✓ Flask installed" -ForegroundColor Green
} else {
    Write-Host "✗ Flask not installed" -ForegroundColor Red
    exit 1
}

if ($packages -match "requests") {
    Write-Host "✓ Requests installed" -ForegroundColor Green
} else {
    Write-Host "✗ Requests not installed" -ForegroundColor Red
    exit 1
}

if ($packages -match "beautifulsoup4") {
    Write-Host "✓ BeautifulSoup4 installed" -ForegroundColor Green
} else {
    Write-Host "✗ BeautifulSoup4 not installed" -ForegroundColor Red
    exit 1
}

# Check app files
if (Test-Path "app\portable.py") {
    Write-Host "✓ portable.py found" -ForegroundColor Green
} else {
    Write-Host "✗ portable.py missing" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "All checks passed! ✓" -ForegroundColor Green
Write-Host "You can now run the server using:" -ForegroundColor Cyan
Write-Host "  .\start-13ft.ps1" -ForegroundColor Yellow
Write-Host "or" -ForegroundColor Cyan
Write-Host "  start-13ft.bat" -ForegroundColor Yellow
