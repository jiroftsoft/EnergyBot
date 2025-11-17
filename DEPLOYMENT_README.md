# 🚀 راهنمای کامل Deploy روی سرور mehranyad.ir

## 📦 فایل‌های آماده شده

1. **deploy.sh** - اسکریپت نصب خودکار
2. **supervisor.conf** - تنظیمات Supervisor
3. **nginx.conf** - تنظیمات Nginx
4. **backup.sh** - اسکریپت پشتیبان‌گیری
5. **PLESK_SETUP.md** - کارهایی که باید در Plesk انجام دهید

---

## 🎯 مراحل Deployment

### مرحله 1: کارهای Plesk (شما انجام دهید)

**فقط این کارها را در Plesk انجام دهید:**

1. ✅ **فعال‌سازی SSL Certificate**
   - Plesk → Domains → mehranyad.ir → SSL/TLS Settings
   - Let's Encrypt را نصب کنید
   - Redirect HTTP to HTTPS را فعال کنید

2. ✅ **بررسی دسترسی SSH**
   - مطمئن شوید که دسترسی SSH دارید

**بعد از این کارها، به من اطلاع دهید تا ادامه دهم.**

---

### مرحله 2: آپلود فایل‌ها (من انجام می‌دهم)

**از طریق SSH:**

```bash
# 1. اتصال به سرور
ssh user@mehranyad.ir

# 2. ساخت پوشه پروژه
sudo mkdir -p /var/www/energybot
sudo chown -R $USER:$USER /var/www/energybot
cd /var/www/energybot

# 3. آپلود فایل‌ها (از کامپیوتر محلی)
# با استفاده از scp یا FileZilla
```

**یا از طریق Plesk File Manager:**
- تمام فایل‌های پروژه را در `/var/www/energybot` آپلود کنید

---

### مرحله 3: نصب و راه‌اندازی (من انجام می‌دهم)

```bash
cd /var/www/energybot

# 1. اجرای اسکریپت نصب
chmod +x deploy.sh
./deploy.sh

# 2. ویرایش .env
nano .env
# مقادیر را تنظیم کنید:
# - TELEGRAM_BOT_TOKEN
# - ZARINPAL_MERCHANT_ID
# - ZARINPAL_CALLBACK_URL=https://mehranyad.ir/zarinpal/callback
# - ZARINPAL_SANDBOX=false

# 3. نصب Supervisor
sudo cp supervisor.conf /etc/supervisor/conf.d/energybot.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start energybot_web
sudo supervisorctl start energybot_telegram

# 4. تنظیم Nginx (اگر از Nginx استفاده می‌کنید)
sudo cp nginx.conf /etc/nginx/sites-available/energybot
sudo ln -s /etc/nginx/sites-available/energybot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 5. ساخت پوشه لاگ
sudo mkdir -p /var/log/energybot
sudo chown -R www-data:www-data /var/log/energybot

# 6. تنظیم پشتیبان‌گیری (اختیاری)
chmod +x backup.sh
# اضافه کردن به crontab:
# 0 2 * * * /var/www/energybot/backup.sh
```

---

### مرحله 4: تست

```bash
# تست Health Endpoint
curl https://mehranyad.ir/health
# باید: OK

# تست Callback
curl "https://mehranyad.ir/zarinpal/callback?Authority=TEST&Status=OK"
# باید: صفحه HTML با پیام خطا (چون Authority تستی است)

# بررسی وضعیت Supervisor
sudo supervisorctl status
# باید: energybot_web و energybot_telegram RUNNING باشند
```

---

### مرحله 5: تنظیم در زرین‌پال

1. وارد [پنل زرین‌پال](https://next.zarinpal.com/) شوید
2. به بخش **درگاه‌های پرداخت** بروید
3. درگاه خود را انتخاب کنید
4. در **Callback URL** وارد کنید:
   ```
   https://mehranyad.ir/zarinpal/callback
   ```
5. ذخیره کنید

---

## 🔍 عیب‌یابی

### مشکل: سرور کار نمی‌کند

```bash
# بررسی لاگ‌های Supervisor
sudo tail -f /var/log/energybot/energybot_web.out.log
sudo tail -f /var/log/energybot/energybot_telegram.out.log

# بررسی وضعیت Supervisor
sudo supervisorctl status

# راه‌اندازی مجدد
sudo supervisorctl restart energybot_web
sudo supervisorctl restart energybot_telegram
```

### مشکل: Callback کار نمی‌کند

1. بررسی کنید که SSL فعال است
2. بررسی کنید که Callback URL در زرین‌پال درست است
3. لاگ‌های Nginx را چک کنید:
   ```bash
   sudo tail -f /var/log/nginx/energybot_error.log
   ```

### مشکل: ربات کار نمی‌کند

```bash
# بررسی لاگ ربات
sudo tail -f /var/log/energybot/energybot_telegram.err.log

# بررسی Token
# در .env بررسی کنید که TELEGRAM_BOT_TOKEN درست است
```

---

## 📝 نکات مهم

1. **.env فایل:** هرگز در Git commit نکنید
2. **SSL:** بدون SSL، زرین‌پال callback را نمی‌پذیرد
3. **پورت 8000:** فقط از localhost قابل دسترسی باشد
4. **پشتیبان‌گیری:** هر روز ساعت 2 صبح اجرا می‌شود

---

## ✅ چک‌لیست نهایی

- [ ] SSL Certificate فعال شد
- [ ] فایل‌ها آپلود شدند
- [ ] .env تنظیم شد
- [ ] Supervisor نصب و راه‌اندازی شد
- [ ] Nginx تنظیم شد
- [ ] Health endpoint کار می‌کند
- [ ] Callback URL در زرین‌پال تنظیم شد
- [ ] ربات تلگرام کار می‌کند

---

## 🆘 پشتیبانی

اگر مشکلی پیش آمد:
1. لاگ‌ها را بررسی کنید
2. وضعیت Supervisor را چک کنید
3. SSL را بررسی کنید
4. Callback URL را در زرین‌پال بررسی کنید

---

**موفق باشید! 🚀**

