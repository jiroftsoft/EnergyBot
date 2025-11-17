#!/bin/bash
# اسکریپت نصب خودکار برای سرور
# این فایل را در سرور اجرا کنید

set -e

echo "🚀 Starting EnergyBot Deployment..."

# متغیرها
PROJECT_DIR="/var/www/energybot"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_VERSION="python3.11"

# بررسی Python
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo "❌ Python 3.11 not found. Installing..."
    sudo apt update
    sudo apt install -y python3.11 python3.11-venv python3-pip
fi

# ساخت پوشه پروژه
echo "📁 Creating project directory..."
sudo mkdir -p $PROJECT_DIR
sudo chown -R $USER:$USER $PROJECT_DIR

# کپی فایل‌ها (اگر از git استفاده نمی‌کنید)
# این بخش را بعد از آپلود فایل‌ها اجرا کنید

# ساخت Virtual Environment
echo "🐍 Creating virtual environment..."
cd $PROJECT_DIR
$PYTHON_VERSION -m venv venv
source venv/bin/activate

# نصب وابستگی‌ها
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ساخت پوشه لاگ
echo "📝 Creating log directory..."
sudo mkdir -p /var/log/energybot
sudo chown -R $USER:$USER /var/log/energybot

# تنظیم مجوزها
echo "🔐 Setting permissions..."
chmod 600 .env
chmod +x venv/bin/*

echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: python -m app.db.init_db (if needed)"
echo "3. Configure Supervisor (see supervisor.conf)"
echo "4. Configure Nginx (see nginx.conf)"

