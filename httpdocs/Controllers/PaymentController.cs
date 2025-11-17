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

