# ⚡ راهنمای سریع یکپارچه‌سازی

## 🎯 هدف
استفاده از سیستم پرداخت موجود سایت برای ربات تلگرام

---

## 📋 مراحل (3 مرحله)

### مرحله 1: اضافه کردن متد TelegramCallback

**فایل:** `C:\Users\Developer\source\repos\ADMVC\Controllers\PaymentController.cs`

**کد را اضافه کنید:**
```csharp
/// <summary>
/// Callback مخصوص ربات تلگرام
/// </summary>
[HttpGet]
[AllowAnonymous]
public ActionResult TelegramCallback(string authority, string status)
{
    if (string.IsNullOrEmpty(authority) || string.IsNullOrEmpty(status))
    {
        Response.StatusCode = 400;
        return Content("<html><body><h3 style=\"text-align:center;padding:20px;\">پارامترهای بازگشت ناقص است.</h3></body></html>", "text/html");
    }

    // URL سرور Python (از Railway) - این را به‌روزرسانی کنید
    string pythonServerUrl = "https://web-production-3b8ee.up.railway.app";
    string callbackUrl = $"{pythonServerUrl}/zarinpal/callback?Authority={Uri.EscapeDataString(authority)}&Status={Uri.EscapeDataString(status)}";
    
    return Redirect(callbackUrl);
}
```

---

### مرحله 2: اضافه کردن Route

**فایل:** `C:\Users\Developer\source\repos\ADMVC\App_Start\RouteConfig.cs`

**در متد `RegisterRoutes`، قبل از Route پیش‌فرض اضافه کنید:**
```csharp
routes.MapRoute(
    name: "TelegramPaymentCallback",
    url: "payment/telegram/callback",
    defaults: new { controller = "Payment", action = "TelegramCallback" }
);
```

---

### مرحله 3: تنظیم در زرین‌پال

**در پنل زرین‌پال:**
- Callback URL برای پرداخت‌های ربات:
  ```
  https://mehranyad.ir/payment/telegram/callback
  ```

**نکته:** Callback URL موجود سایت (`/Payment/Callback`) دست نخورده می‌ماند.

---

## ✅ تست

بعد از Deploy، این URL را تست کنید:
```
https://mehranyad.ir/payment/telegram/callback?authority=TEST&status=OK
```

باید به سرور Python redirect شود.

---

## 📝 نکات مهم

1. **URL Railway:** حتماً URL Railway را در متد `TelegramCallback` به‌روزرسانی کنید
2. **Build:** بعد از تغییرات، پروژه را Build و Deploy کنید
3. **Callback موجود:** Callback موجود سایت (`/Payment/Callback`) دست نخورده می‌ماند

---

## 🔧 فایل‌های آماده

- **`httpdocs/Controllers/PaymentController_Telegram.cs`** - کد آماده
- **`httpdocs/App_Start/RouteConfig_Telegram.cs`** - Route آماده
- **`INTEGRATION_COMPLETE.md`** - راهنمای کامل

---

**موفق باشید! 🚀**

