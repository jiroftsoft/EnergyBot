# 🎯 راهنمای کامل Callback برای ASP.NET MVC

## 📋 ساختار فایل‌ها

برای پروژه ASP.NET MVC شما، باید این فایل‌ها را اضافه کنید:

---

## 1️⃣ ساخت Controller

### فایل: `Controllers/PaymentController.cs`

```csharp
using System;
using System.Web.Mvc;

namespace YourProjectName.Controllers
{
    public class PaymentController : Controller
    {
        // URL سرور Python (از Railway)
        // این URL را بعد از deploy کردن ربات به‌روزرسانی کنید
        private readonly string pythonServerUrl = "https://web-production-3b8ee.up.railway.app";
        
        /// <summary>
        /// Callback از زرین‌پال - این متد callback را به سرور Python forward می‌کند
        /// </summary>
        /// <param name="Authority">Authority از زرین‌پال</param>
        /// <param name="Status">Status از زرین‌پال (OK یا NOK)</param>
        /// <returns>Redirect به سرور Python</returns>
        [HttpGet]
        [AllowAnonymous]
        public ActionResult ZarinpalCallback(string Authority, string Status)
        {
            // بررسی پارامترها
            if (string.IsNullOrEmpty(Authority) || string.IsNullOrEmpty(Status))
            {
                Response.StatusCode = 400;
                return Content("<html><body><h3 style=\"text-align:center;padding:20px;\">پارامترهای بازگشت ناقص است.</h3></body></html>", "text/html");
            }
            
            // ساخت URL برای forward کردن به سرور Python
            string callbackUrl = $"{pythonServerUrl}/zarinpal/callback?Authority={Uri.EscapeDataString(Authority)}&Status={Uri.EscapeDataString(Status)}";
            
            // Redirect به سرور Python
            return Redirect(callbackUrl);
        }
    }
}
```

---

## 2️⃣ تنظیم Route (اختیاری - اگر Route سفارشی می‌خواهید)

### فایل: `App_Start/RouteConfig.cs`

اگر می‌خواهید Route سفارشی داشته باشید، می‌توانید این را اضافه کنید:

```csharp
public static void RegisterRoutes(RouteCollection routes)
{
    routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

    // Route برای Zarinpal Callback
    routes.MapRoute(
        name: "ZarinpalCallback",
        url: "zarinpal/callback",
        defaults: new { controller = "Payment", action = "ZarinpalCallback" }
    );

    // Route پیش‌فرض
    routes.MapRoute(
        name: "Default",
        url: "{controller}/{action}/{id}",
        defaults: new { controller = "Home", action = "Index", id = UrlParameter.Optional }
    );
}
```

**نکته:** اگر Route اضافه نکنید، URL به صورت `/Payment/ZarinpalCallback` خواهد بود که هم کار می‌کند.

---

## 3️⃣ تنظیم در زرین‌پال

در پنل زرین‌پال، Callback URL را به یکی از این‌ها تنظیم کنید:

### گزینه 1: با Route (اگر Route اضافه کردید)
```
https://mehranyad.ir/zarinpal/callback
```

### گزینه 2: بدون Route (Route پیش‌فرض)
```
https://mehranyad.ir/Payment/ZarinpalCallback
```

---

## 4️⃣ به‌روزرسانی URL سرور Python

بعد از اینکه Railway URL را دریافت کردید، در `PaymentController.cs` این خط را به‌روزرسانی کنید:

```csharp
private readonly string pythonServerUrl = "https://YOUR-RAILWAY-URL.railway.app";
```

---

## 5️⃣ تست

### تست محلی:
```
http://localhost:PORT/Payment/ZarinpalCallback?Authority=TEST&Status=OK
```
یا اگر Route اضافه کردید:
```
http://localhost:PORT/zarinpal/callback?Authority=TEST&Status=OK
```

### تست Production:
```
https://mehranyad.ir/Payment/ZarinpalCallback?Authority=TEST&Status=OK
```
یا:
```
https://mehranyad.ir/zarinpal/callback?Authority=TEST&Status=OK
```

باید به سرور Python redirect شود.

---

## 📝 مراحل نصب

### مرحله 1: اضافه کردن Controller

1. در Visual Studio، به پوشه `Controllers` بروید
2. راست کلیک → **Add** → **Controller**
3. نام: `PaymentController`
4. کد بالا را در آن قرار دهید
5. URL سرور Python را به‌روزرسانی کنید

### مرحله 2: تنظیم Route (اختیاری)

1. فایل `RouteConfig.cs` را باز کنید
2. Route بالا را اضافه کنید (قبل از Route پیش‌فرض)

### مرحله 3: Build و Deploy

1. پروژه را Build کنید
2. به هاست Deploy کنید
3. در زرین‌پال Callback URL را تنظیم کنید

---

## ✅ مزایای این روش

- ✅ **سازگار با ASP.NET MVC**
- ✅ **استفاده از Controller و Route**
- ✅ **قابل نگهداری و تست**
- ✅ **امنیت بهتر** (می‌توانید validation اضافه کنید)

---

## 🔒 نکات امنیتی (اختیاری)

اگر می‌خواهید امنیت بیشتری اضافه کنید:

```csharp
[HttpGet]
[AllowAnonymous]
[ValidateAntiForgeryToken] // اگر می‌خواهید CSRF protection داشته باشید
public ActionResult ZarinpalCallback(string Authority, string Status)
{
    // می‌توانید IP زرین‌پال را validate کنید
    // می‌توانید Authority را در دیتابیس خود چک کنید
    // و غیره...
    
    // کد اصلی...
}
```

---

## 🎯 خلاصه

1. ✅ `PaymentController.cs` را بسازید
2. ✅ URL سرور Python را به‌روزرسانی کنید
3. ✅ Route اضافه کنید (اختیاری)
4. ✅ در زرین‌پال Callback URL را تنظیم کنید
5. ✅ تست کنید

---

**موفق باشید! 🚀**

