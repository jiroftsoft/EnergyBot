#!/bin/bash
# اسکریپت پشتیبان‌گیری از دیتابیس
# این فایل را در cron job قرار دهید

BACKUP_DIR="/var/backups/energybot"
PROJECT_DIR="/var/www/energybot"
DATE=$(date +%Y%m%d_%H%M%S)

# ساخت پوشه backup
mkdir -p $BACKUP_DIR

# پشتیبان‌گیری از دیتابیس
if [ -f "$PROJECT_DIR/gym_bot.db" ]; then
    cp "$PROJECT_DIR/gym_bot.db" "$BACKUP_DIR/gym_bot_$DATE.db"
    
    # حذف backup های قدیمی‌تر از 30 روز
    find $BACKUP_DIR -name "gym_bot_*.db" -mtime +30 -delete
    
    echo "✅ Backup created: gym_bot_$DATE.db"
else
    echo "⚠️  Database file not found!"
fi

# پشتیبان‌گیری از .env (اختیاری - با احتیاط!)
# cp "$PROJECT_DIR/.env" "$BACKUP_DIR/env_$DATE.backup"

