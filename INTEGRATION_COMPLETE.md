# 🔗 راهنمای کامل یکپارچه‌سازی با سیستم موجود mehranyad.ir

## 📋 خلاصه سیستم موجود

### ساختار فعلی:
- ✅ **PaymentController.Callback** - پردازش callback از زرین‌پال
- ✅ **Transaction Model** - ذخیره تراکنش‌ها
- ✅ **Order Model** - مدیریت سفارش‌ها
- ✅ **ZarinpalGateway** - اتصال به زرین‌پال
- ✅ **PaymentService** - منطق پرداخت

### Callback URL فعلی:
```
https://mehranyad.ir/Payment/Callback?authority=...&status=...
```

---

## 🎯 راه‌حل پیشنهادی: Callback مشترک + Metadata

### مزایا:
- ✅ استفاده از سیستم موجود
- ✅ یکپارچه با دیتابیس موجود
- ✅ بدون تغییر در کدهای موجود
- ✅ مدیریت متمرکز

---

## 📝 پیاده‌سازی

### مرحله 1: Extend کردن PaymentController.Callback

در `PaymentController.cs` موجود، متد `Callback` را extend کنید:

```csharp
public async Task<ActionResult> Callback(string authority, string status)
{
    var transaction = await _paymentService.FinalizePaymentAsync(authority, status);

    if (transaction == null)
    {
        return new HttpStatusCodeResult(HttpStatusCode.BadRequest, "Transaction not found.");
    }

    // بررسی اینکه آیا از ربات تلگرام آمده یا نه
    // می‌توانیم از metadata در Transaction استفاده کنیم
    // یا یک فیلد جدید اضافه کنیم: Source (Website/Telegram)
    
    bool isFromTelegram = transaction.Source == "Telegram"; // اگر فیلد Source اضافه کردید
    // یا از metadata استفاده کنید:
    // bool isFromTelegram = !string.IsNullOrEmpty(transaction.Metadata) && 
    //                       transaction.Metadata.Contains("telegram");

    if (transaction.Status == TransactionStatus.Succeeded)
    {
        if (isFromTelegram)
        {
            // اگر از ربات آمده، به ربات اطلاع دهید
            await NotifyTelegramBot(transaction);
            
            // Redirect به صفحه موفقیت ربات (یا یک صفحه ساده)
            return Redirect($"https://t.me/EnergyGym_Bot?start=payment_success_{transaction.Id}");
        }
        else
        {
            // اگر از سایت آمده، مثل قبل
            return View("Success", transaction.Order);
        }
    }
    else
    {
        if (isFromTelegram)
        {
            // اطلاع به ربات
            await NotifyTelegramBot(transaction);
            return Redirect($"https://t.me/EnergyGym_Bot?start=payment_failed_{transaction.Id}");
        }
        else
        {
            return View("Failure", transaction.Order);
        }
    }
}

// متد جدید برای اطلاع به ربات
private async Task NotifyTelegramBot(Transaction transaction)
{
    try
    {
        // از Webhook یا API ربات استفاده کنید
        // یا از یک Service مشترک
        var botService = new TelegramBotService();
        await botService.NotifyPaymentResult(transaction);
    }
    catch (Exception ex)
    {
        // Log error but don't fail the payment flow
        // Log.Error(ex, "Failed to notify Telegram bot");
    }
}
```

---

### مرحله 2: اضافه کردن فیلد Source به Transaction (اختیاری)

اگر می‌خواهید منبع پرداخت را ذخیره کنید:

**Migration:**
```csharp
public partial class AddSourceToTransaction : DbMigration
{
    public override void Up()
    {
        AddColumn("dbo.Transactions", "Source", c => c.String(maxLength: 50));
    }

    public override void Down()
    {
        DropColumn("dbo.Transactions", "Source");
    }
}
```

**Model:**
```csharp
public class Transaction
{
    // ... فیلدهای موجود ...
    public string Source { get; set; } // "Website" or "Telegram"
}
```

---

### مرحله 3: ساخت Callback جداگانه برای ربات (گزینه جایگزین)

اگر نمی‌خواهید Callback موجود را تغییر دهید:

**در PaymentController.cs:**
```csharp
/// <summary>
/// Callback مخصوص ربات تلگرام
/// </summary>
[AllowAnonymous]
public async Task<ActionResult> TelegramCallback(string authority, string status)
{
    // Forward به سرور Python
    string pythonServerUrl = "https://web-production-3b8ee.up.railway.app";
    string callbackUrl = $"{pythonServerUrl}/zarinpal/callback?Authority={Uri.EscapeDataString(authority)}&Status={Uri.EscapeDataString(status)}";
    
    return Redirect(callbackUrl);
}
```

**در RouteConfig.cs:**
```csharp
routes.MapRoute(
    name: "TelegramPaymentCallback",
    url: "payment/telegram/callback",
    defaults: new { controller = "Payment", action = "TelegramCallback" }
);
```

**در زرین‌پال:**
- برای پرداخت‌های ربات: `https://mehranyad.ir/payment/telegram/callback`
- برای پرداخت‌های سایت: `https://mehranyad.ir/Payment/Callback` (موجود)

---

## 🔧 راه‌حل پیشنهادی: استفاده از دیتابیس مشترک

### مزایا:
- ✅ یکپارچه با سیستم موجود
- ✅ مدیریت متمرکز
- ✅ گزارش‌گیری یکپارچه

### پیاده‌سازی:

1. **در ربات Python:**
   - به جای SQLite، از SQL Server استفاده کنید
   - Connection String را به دیتابیس موجود متصل کنید

2. **در app/core/config.py:**
   ```python
   DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
   ```

3. **استفاده از جداول موجود:**
   - می‌توانید از جداول `Transactions` و `Orders` موجود استفاده کنید
   - یا جداول جدید با prefix بسازید (مثلاً `TelegramTransactions`)

---

## 📋 گزینه‌های یکپارچه‌سازی

### گزینه 1: Callback مشترک (توصیه می‌شود)
- ✅ یک Callback برای همه
- ✅ مدیریت متمرکز
- ⚠️ نیاز به تغییر کد موجود

### گزینه 2: Callback جداگانه
- ✅ بدون تغییر در کد موجود
- ✅ ساده‌تر
- ⚠️ دو Callback URL

### گزینه 3: دیتابیس مشترک
- ✅ یکپارچه کامل
- ✅ گزارش‌گیری متمرکز
- ⚠️ نیاز به تنظیمات بیشتر

---

## 🎯 توصیه نهایی

**برای شروع سریع:**
1. از **Callback جداگانه** استفاده کنید (`TelegramCallback`)
2. بعداً می‌توانید به **Callback مشترک** یا **دیتابیس مشترک** مهاجرت کنید

**برای یکپارچه‌سازی کامل:**
1. **دیتابیس مشترک** + **Callback مشترک**
2. همه چیز در یک جا

---

## 📝 مراحل عملی

### اگر Callback جداگانه می‌خواهید:

1. **PaymentController.cs** را باز کنید
2. متد `TelegramCallback` را اضافه کنید (کد بالا)
3. Route را اضافه کنید
4. در زرین‌پال، Callback URL را تنظیم کنید
5. در ربات، Callback URL را به `https://mehranyad.ir/payment/telegram/callback` تنظیم کنید

---

**کدام گزینه را ترجیح می‌دهید؟ من می‌توانم کدهای کامل را برای هر کدام بنویسم! 🚀**

