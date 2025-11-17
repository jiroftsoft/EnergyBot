<?php
/**
 * Callback Forwarder برای زرین‌پال
 * این فایل callback را از mehranyad.ir به سرور Python forward می‌کند
 * 
 * استفاده:
 * 1. این فایل را در httpdocs آپلود کنید
 * 2. URL سرور Python را در متغیر $pythonServerUrl تنظیم کنید
 * 3. در زرین‌پال، Callback URL را به https://mehranyad.ir/zarinpal_callback.php تنظیم کنید
 */

// URL سرور Python (از Railway/Render/VPS)
// این URL را بعد از deploy کردن ربات به‌روزرسانی کنید
$pythonServerUrl = 'https://YOUR-PYTHON-SERVER-URL.railway.app';
// مثال: 'https://energybot-production.up.railway.app'

// دریافت پارامترها از زرین‌پال
$authority = $_GET['Authority'] ?? '';
$status = $_GET['Status'] ?? '';

// بررسی پارامترها
if (empty($authority) || empty($status)) {
    http_response_code(400);
    die('<html><body><h3 style="text-align:center;padding:20px;">پارامترهای بازگشت ناقص است.</h3></body></html>');
}

// ساخت URL برای forward کردن
$callbackUrl = $pythonServerUrl . '/zarinpal/callback?' . http_build_query([
    'Authority' => $authority,
    'Status' => $status
]);

// Forward کردن درخواست
header('Location: ' . $callbackUrl);
exit;
?>

