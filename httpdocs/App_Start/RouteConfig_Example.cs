using System.Web.Mvc;
using System.Web.Routing;

namespace YourProjectName.App_Start
{
    /// <summary>
    /// مثال Route Configuration برای Zarinpal Callback
    /// این کد را در فایل RouteConfig.cs خود اضافه کنید
    /// </summary>
    public class RouteConfig_Example
    {
        public static void RegisterRoutes(RouteCollection routes)
        {
            routes.IgnoreRoute("{resource}.axd/{*pathInfo}");

            // Route برای Zarinpal Callback (قبل از Route پیش‌فرض)
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
    }
}

