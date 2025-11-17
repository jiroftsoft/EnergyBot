# ☁️ راه‌حل: اجرا روی Cloud + Callback در دامین شما

## 🎯 راه‌حل پیشنهادی

از آنجایی که هاست شما از Python پشتیبانی نمی‌کند، می‌توانیم:

1. **ربات و FastAPI را روی یک سرویس Cloud رایگان/ارزان اجرا کنیم**
2. **یک صفحه ساده در دامین `mehranyad.ir` بسازیم که callback را forward کند**

---

## 🚀 گزینه 1: استفاده از Railway (رایگان تا 500 ساعت/ماه)

### مزایا:
- ✅ رایگان برای شروع
- ✅ نصب خودکار
- ✅ SSL خودکار
- ✅ آسان برای deploy

### مراحل:

1. **ثبت‌نام در Railway:**
   - به [railway.app](https://railway.app) بروید
   - با GitHub ثبت‌نام کنید

2. **Deploy پروژه:**
   - پروژه را به GitHub push کنید
   - در Railway، New Project → Deploy from GitHub
   - Repository را انتخاب کنید
   - Railway خودکار detect می‌کند و deploy می‌کند

3. **تنظیم Environment Variables:**
   - در Railway → Variables
   - تمام متغیرهای `.env` را اضافه کنید

4. **دریافت URL:**
   - Railway یک URL می‌دهد مثل: `energybot-production.up.railway.app`
   - این URL را برای callback استفاده می‌کنیم

---

## 🌐 گزینه 2: استفاده از Render (رایگان)

### مراحل:

1. **ثبت‌نام در Render:**
   - به [render.com](https://render.com) بروید
   - ثبت‌نام کنید

2. **Deploy:**
   - New → Web Service
   - Repository را connect کنید
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.web_admin.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables:**
   - تمام متغیرهای `.env` را اضافه کنید

---

## 💻 گزینه 3: VPS ارزان (مثل DigitalOcean, Vultr)

### هزینه: حدود $5-6 در ماه

### مراحل:

1. **خرید VPS:**
   - DigitalOcean Droplet ($5/ماه)
   - یا Vultr ($6/ماه)

2. **نصب:**
   - از راهنمای `DEPLOYMENT_README.md` استفاده کنید
   - یا از `deploy.sh` استفاده کنید

---

## 🔗 راه‌حل: Callback در دامین شما

بعد از اینکه ربات روی Cloud اجرا شد، یک صفحه ساده در `mehranyad.ir` می‌سازیم که callback را forward کند.

### گزینه A: استفاده از PHP (ساده‌تر)

یک فایل `zarinpal_callback.php` در `httpdocs`:

```php
<?php
// zarinpal_callback.php
// این فایل callback را به سرور Python forward می‌کند

$authority = $_GET['Authority'] ?? '';
$status = $_GET['Status'] ?? '';

if (empty($authority) || empty($status)) {
    die('<h3>پارامترهای بازگشت ناقص است.</h3>');
}

// URL سرور Python (از Railway/Render/VPS)
$pythonServerUrl = 'https://energybot-production.up.railway.app';

// Forward کردن درخواست
$callbackUrl = $pythonServerUrl . '/zarinpal/callback?' . http_build_query([
    'Authority' => $authority,
    'Status' => $status
]);

// Redirect
header('Location: ' . $callbackUrl);
exit;
?>
```

### گزینه B: استفاده از ASP.NET (برای سایت شما)

یک فایل `zarinpal_callback.aspx`:

```aspx
<%@ Page Language="C#" %>
<%
    string authority = Request.QueryString["Authority"] ?? "";
    string status = Request.QueryString["Status"] ?? "";
    
    if (string.IsNullOrEmpty(authority) || string.IsNullOrEmpty(status))
    {
        Response.Write("<h3>پارامترهای بازگشت ناقص است.</h3>");
        Response.End();
        return;
    }
    
    // URL سرور Python
    string pythonServerUrl = "https://energybot-production.up.railway.app";
    string callbackUrl = pythonServerUrl + "/zarinpal/callback?Authority=" + 
                        Server.UrlEncode(authority) + "&Status=" + Server.UrlEncode(status);
    
    Response.Redirect(callbackUrl);
%>
```

---

## 📝 تنظیمات

### 1. در زرین‌پال:
- Callback URL را به این تنظیم کنید:
  ```
  https://mehranyad.ir/zarinpal_callback.php
  ```
  یا
  ```
  https://mehranyad.ir/zarinpal_callback.aspx
  ```

### 2. در فایل PHP/ASP.NET:
- URL سرور Python را به‌روزرسانی کنید

---

## ✅ مزایای این راه‌حل

1. ✅ **هیچ تغییری در هاست شما نیاز نیست**
2. ✅ **دامین شما (`mehranyad.ir`) در callback URL استفاده می‌شود**
3. ✅ **ربات روی Cloud اجرا می‌شود (رایگان یا ارزان)**
4. ✅ **ساده و قابل نگهداری**

---

## 🎯 توصیه

**برای شروع:** Railway یا Render (رایگان)  
**برای Production:** VPS کوچک ($5-6/ماه)

---

**کدام گزینه را ترجیح می‌دهید؟ من می‌توانم راهنمای دقیق‌تر برای هر کدام بدهم.**

