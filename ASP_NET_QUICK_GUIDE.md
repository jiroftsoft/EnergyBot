# ⚡ راهنمای سریع - ASP.NET MVC

## 🎯 فقط 3 مرحله

### مرحله 1: اضافه کردن Controller

1. در Visual Studio، به پوشه `Controllers` بروید
2. فایل `PaymentController.cs` را بسازید (یا از فایل آماده استفاده کنید)
3. **مهم:** URL سرور Python را به‌روزرسانی کنید:
   ```csharp
   private readonly string pythonServerUrl = "https://web-production-3b8ee.up.railway.app";
   ```

### مرحله 2: تنظیم Route (اختیاری اما توصیه می‌شود)

در فایل `RouteConfig.cs`، قبل از Route پیش‌فرض این را اضافه کنید:

```csharp
routes.MapRoute(
    name: "ZarinpalCallback",
    url: "zarinpal/callback",
    defaults: new { controller = "Payment", action = "ZarinpalCallback" }
);
```

**نتیجه:** URL شما می‌شود: `https://mehranyad.ir/zarinpal/callback`

### مرحله 3: تنظیم در زرین‌پال

در پنل زرین‌پال، Callback URL را تنظیم کنید:

**اگر Route اضافه کردید:**
```
https://mehranyad.ir/zarinpal/callback
```

**اگر Route اضافه نکردید:**
```
https://mehranyad.ir/Payment/ZarinpalCallback
```

---

## 📁 فایل‌های آماده

1. **`httpdocs/Controllers/PaymentController.cs`** - Controller آماده
2. **`httpdocs/App_Start/RouteConfig_Example.cs`** - مثال Route
3. **`ASP_NET_MVC_SETUP.md`** - راهنمای کامل

---

## ✅ تست

بعد از Deploy، این URL را تست کنید:

```
https://mehranyad.ir/zarinpal/callback?Authority=TEST&Status=OK
```

باید به سرور Python redirect شود.

---

## 🔧 نکات مهم

1. **Namespace:** در `PaymentController.cs`، `YourProjectName` را با نام پروژه خود جایگزین کنید
2. **URL Railway:** حتماً URL Railway را در Controller به‌روزرسانی کنید
3. **Build:** بعد از تغییرات، پروژه را Build و Deploy کنید

---

**موفق باشید! 🚀**

