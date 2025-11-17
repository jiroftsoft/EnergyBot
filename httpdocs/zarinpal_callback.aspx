<%@ Page Language="C#" %>
<%
    /**
     * Callback Forwarder برای زرین‌پال
     * این فایل callback را از mehranyad.ir به سرور Python forward می‌کند
     * 
     * استفاده:
     * 1. این فایل را در httpdocs آپلود کنید
     * 2. URL سرور Python را در متغیر pythonServerUrl تنظیم کنید
     * 3. در زرین‌پال، Callback URL را به https://mehranyad.ir/zarinpal_callback.aspx تنظیم کنید
     */
    
    // URL سرور Python (از Railway/Render/VPS)
    // این URL را بعد از deploy کردن ربات به‌روزرسانی کنید
    string pythonServerUrl = "https://YOUR-PYTHON-SERVER-URL.railway.app";
    // مثال: "https://energybot-production.up.railway.app"
    
    // دریافت پارامترها از زرین‌پال
    string authority = Request.QueryString["Authority"] ?? "";
    string status = Request.QueryString["Status"] ?? "";
    
    // بررسی پارامترها
    if (string.IsNullOrEmpty(authority) || string.IsNullOrEmpty(status))
    {
        Response.StatusCode = 400;
        Response.Write("<html><body><h3 style=\"text-align:center;padding:20px;\">پارامترهای بازگشت ناقص است.</h3></body></html>");
        Response.End();
        return;
    }
    
    // ساخت URL برای forward کردن
    string callbackUrl = pythonServerUrl + "/zarinpal/callback?Authority=" + 
                        Server.UrlEncode(authority) + "&Status=" + Server.UrlEncode(status);
    
    // Forward کردن درخواست
    Response.Redirect(callbackUrl);
%>

