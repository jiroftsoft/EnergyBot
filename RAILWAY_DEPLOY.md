# 🚂 راهنمای Deploy روی Railway (رایگان)

## 🎯 چرا Railway؟

- ✅ **رایگان** تا 500 ساعت در ماه
- ✅ **نصب خودکار** از GitHub
- ✅ **SSL خودکار**
- ✅ **ساده و سریع**

---

## 📋 مراحل Deploy

### مرحله 1: آماده‌سازی GitHub

1. **ساخت Repository:**
   - به GitHub بروید
   - New Repository بسازید
   - نام: `energybot` (یا هر نامی که می‌خواهید)

2. **Push کردن کد:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/energybot.git
   git push -u origin main
   ```

---

### مرحله 2: ساخت Railway Account

1. به [railway.app](https://railway.app) بروید
2. **Start a New Project** را بزنید
3. **Deploy from GitHub repo** را انتخاب کنید
4. Repository را انتخاب کنید
5. Railway خودکار detect می‌کند و deploy می‌کند

---

### مرحله 3: تنظیم Environment Variables

1. در Railway → Project → Variables
2. این متغیرها را اضافه کنید:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./gym_bot.db
ZARINPAL_MERCHANT_ID=your_zarinpal_merchant_id_here
ZARINPAL_CALLBACK_URL=https://mehranyad.ir/zarinpal_callback.php
ZARINPAL_SANDBOX=false
ADMIN_USERNAME=admin
ADMIN_PASSWORD=change_me_secure_password
LOG_LEVEL=INFO
```

---

### مرحله 4: تنظیم Start Command

1. در Railway → Settings → Deploy
2. **Start Command** را تنظیم کنید:

```
uvicorn app.web_admin.main:app --host 0.0.0.0 --port $PORT
```

**نکته:** Railway خودکار `$PORT` را تنظیم می‌کند.

---

### مرحله 5: تنظیم برای Telegram Bot

Railway فقط یک Web Service می‌سازد. برای ربات تلگرام:

**گزینه 1: استفاده از Worker (توصیه می‌شود)**

1. در Railway → **New Service** → **Empty Service**
2. نام: `telegram-bot`
3. **Start Command:**
   ```
   python -m app.telegram.main
   ```
4. Environment Variables را از Service اصلی کپی کنید

**گزینه 2: اجرای هر دو در یک Service (ساده‌تر اما کمتر بهینه)**

از فایل `start.sh` استفاده کنید و Start Command را به `bash start.sh` تغییر دهید.

---

### مرحله 6: دریافت URL

1. در Railway → Settings → Domains
2. Railway یک URL می‌دهد مثل:
   ```
   https://energybot-production.up.railway.app
   ```
3. این URL را یادداشت کنید

---

### مرحله 7: تنظیم Callback در دامین شما

1. فایل `zarinpal_callback.php` یا `zarinpal_callback.aspx` را در `httpdocs` آپلود کنید
2. URL سرور Python را در فایل به‌روزرسانی کنید:

```php
$pythonServerUrl = 'https://energybot-production.up.railway.app';
```

3. در زرین‌پال، Callback URL را تنظیم کنید:
   ```
   https://mehranyad.ir/zarinpal_callback.php
   ```
   یا
   ```
   https://mehranyad.ir/zarinpal_callback.aspx
   ```

---

## 🔍 تست

### 1. تست Health Endpoint:
```
https://energybot-production.up.railway.app/health
```
باید: `OK`

### 2. تست Callback:
```
https://mehranyad.ir/zarinpal_callback.php?Authority=TEST&Status=OK
```
باید: به سرور Python redirect شود

---

## 📝 فایل‌های مورد نیاز

برای Railway، باید این فایل‌ها را اضافه کنید:

### 1. `Procfile` (اختیاری - برای Heroku style)
```
web: uvicorn app.web_admin.main:app --host 0.0.0.0 --port $PORT
worker: python -m app.telegram.main
```

### 2. `runtime.txt` (اگر Python version خاصی می‌خواهید)
```
python-3.11.0
```

### 3. `railway.json` (برای تنظیمات پیشرفته)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.web_admin.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## ⚠️ نکات مهم

1. **Database:** Railway هر بار restart می‌شود، پس SQLite ممکن است data را از دست بدهد
   - **راه‌حل:** از Railway PostgreSQL استفاده کنید (رایگان)
   - یا از یک سرویس database خارجی استفاده کنید

2. **Logs:** در Railway → Deployments → Logs می‌توانید لاگ‌ها را ببینید

3. **Environment Variables:** هرگز در کد commit نکنید

4. **Port:** Railway خودکار `$PORT` را تنظیم می‌کند

---

## 🔧 عیب‌یابی

### مشکل: Deploy failed
- لاگ‌ها را در Railway → Deployments → Logs بررسی کنید
- بررسی کنید که `requirements.txt` درست است

### مشکل: Bot کار نمی‌کند
- بررسی کنید که Worker Service ساخته شده
- Environment Variables را بررسی کنید

### مشکل: Callback کار نمی‌کند
- URL سرور Python را در فایل PHP/ASP.NET بررسی کنید
- SSL را بررسی کنید

---

## 💰 هزینه

- **رایگان:** 500 ساعت در ماه
- **Pro:** $20/ماه (برای استفاده بیشتر)

برای شروع، رایگان کافی است!

---

**موفق باشید! 🚀**

