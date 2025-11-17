using System.Web.Mvc;
using System.Web.Routing;

namespace ADMVC.App_Start
{
    /// <summary>
    /// این Route را در فایل RouteConfig.cs موجود اضافه کنید
    /// قبل از Route پیش‌فرض (Default)
    /// </summary>
    public static class RouteConfig_Telegram
    {
        /// <summary>
        /// Route برای Callback ربات تلگرام
        /// این Route را در متد RegisterRoutes اضافه کنید
        /// </summary>
        public static void AddTelegramCallbackRoute(RouteCollection routes)
        {
            routes.MapRoute(
                name: "TelegramPaymentCallback",
                url: "payment/telegram/callback",
                defaults: new { controller = "Payment", action = "TelegramCallback" }
            );
        }
    }
}

