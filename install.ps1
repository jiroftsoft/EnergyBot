# اسکریپت نصب خودکار برای Windows Host
# این فایل را در PowerShell اجرا کنید: .\install.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting EnergyBot Installation on Windows..." -ForegroundColor Green

# متغیرها
$ProjectDir = $PSScriptRoot
$VenvDir = Join-Path $ProjectDir "venv"
$PythonExe = "python"

# بررسی Python
Write-Host "`n🔍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = & $PythonExe --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.11+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# ساخت Virtual Environment
Write-Host "`n🐍 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path $VenvDir) {
    Write-Host "⚠️  Virtual environment already exists. Skipping..." -ForegroundColor Yellow
} else {
    & $PythonExe -m venv $VenvDir
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# فعال‌سازی Virtual Environment
Write-Host "`n📦 Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $VenvDir "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
} else {
    Write-Host "❌ Cannot find activation script" -ForegroundColor Red
    exit 1
}

# نصب وابستگی‌ها
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
& "$VenvDir\Scripts\pip.exe" install --upgrade pip
& "$VenvDir\Scripts\pip.exe" install -r requirements.txt

# ساخت پوشه لاگ
Write-Host "`n📝 Creating log directory..." -ForegroundColor Yellow
$logsDir = Join-Path $ProjectDir "logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
    Write-Host "✅ Log directory created" -ForegroundColor Green
} else {
    Write-Host "⚠️  Log directory already exists" -ForegroundColor Yellow
}

# بررسی فایل .env
Write-Host "`n🔐 Checking .env file..." -ForegroundColor Yellow
$envFile = Join-Path $ProjectDir ".env"
$envExample = Join-Path $ProjectDir ".env.example"

if (-not (Test-Path $envFile)) {
    if (Test-Path $envExample) {
        Copy-Item $envExample $envFile
        Write-Host "✅ Created .env from .env.example" -ForegroundColor Green
        Write-Host "⚠️  Please edit .env file with your actual values!" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️  .env.example not found. Please create .env manually." -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
}

# تنظیم مجوزها
Write-Host "`n🔒 Setting permissions..." -ForegroundColor Yellow
if (Test-Path $envFile) {
    icacls $envFile /inheritance:r /grant:r "$env:USERNAME:(R)" | Out-Null
    Write-Host "✅ .env file permissions set" -ForegroundColor Green
}

Write-Host "`n✅ Installation completed!" -ForegroundColor Green
Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your actual values" -ForegroundColor White
Write-Host "2. Configure IIS/Plesk for reverse proxy" -ForegroundColor White
Write-Host "3. Set up Windows Task Scheduler or NSSM" -ForegroundColor White
Write-Host "4. Test the installation" -ForegroundColor White
Write-Host "`nSee WINDOWS_HOST_SETUP.md for detailed instructions." -ForegroundColor Yellow

