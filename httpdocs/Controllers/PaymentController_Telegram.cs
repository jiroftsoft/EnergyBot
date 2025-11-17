using System;
using System.Threading.Tasks;
using System.Web.Mvc;

namespace ADMVC.Controllers
{
    /// <summary>
    /// این فایل را در PaymentController.cs موجود اضافه کنید
    /// یا به عنوان یک متد جدید در همان Controller استفاده کنید
    /// </summary>
    public partial class PaymentController : Controller
    {
        /// <summary>
        /// Callback مخصوص ربات تلگرام
        /// این متد callback را از زرین‌پال دریافت می‌کند و به سرور Python forward می‌کند
        /// </summary>
        /// <param name="authority">Authority از زرین‌پال</param>
        /// <param name="status">Status از زرین‌پال (OK یا NOK)</param>
        /// <returns>Redirect به سرور Python</returns>
        [HttpGet]
        [AllowAnonymous]
        public ActionResult TelegramCallback(string authority, string status)
        {
            // بررسی پارامترها
            if (string.IsNullOrEmpty(authority) || string.IsNullOrEmpty(status))
            {
                Response.StatusCode = 400;
                return Content("<html><body><h3 style=\"text-align:center;padding:20px;\">پارامترهای بازگشت ناقص است.</h3></body></html>", "text/html");
            }

            // URL سرور Python (از Railway)
            // این URL را بعد از deploy کردن ربات به‌روزرسانی کنید
            string pythonServerUrl = "https://web-production-3b8ee.up.railway.app";

            // ساخت URL برای forward کردن به سرور Python
            string callbackUrl = $"{pythonServerUrl}/zarinpal/callback?Authority={Uri.EscapeDataString(authority)}&Status={Uri.EscapeDataString(status)}";

            // Redirect به سرور Python
            return Redirect(callbackUrl);
        }
    }
}

