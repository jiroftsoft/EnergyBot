"""اسکریپت تست برای بررسی صحت تنظیمات Webhook"""
import asyncio
import sys
from pathlib import Path

import httpx
from aiogram import Bot

from app.core.config import settings


async def test_health():
    """تست Health Endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200 and response.text == "OK":
                print("✅ Health endpoint works!")
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False


async def test_callback():
    """تست Callback Endpoint"""
    print("\n🔍 Testing Callback Endpoint...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "http://localhost:8000/zarinpal/callback",
                params={"Authority": "TEST_AUTHORITY", "Status": "OK"},
            )
            if response.status_code in (200, 400, 404):
                print(f"✅ Callback endpoint responds (status: {response.status_code})")
                return True
            else:
                print(f"❌ Callback endpoint failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Callback endpoint error: {e}")
        return False


def test_config():
    """تست تنظیمات"""
    print("\n🔍 Testing Configuration...")
    issues = []
    
    if not settings.TELEGRAM_BOT_TOKEN:
        issues.append("❌ TELEGRAM_BOT_TOKEN is not set")
    else:
        print("✅ TELEGRAM_BOT_TOKEN is set")
    
    if not settings.ZARINPAL_MERCHANT_ID:
        issues.append("❌ ZARINPAL_MERCHANT_ID is not set")
    else:
        print(f"✅ ZARINPAL_MERCHANT_ID is set: {settings.ZARINPAL_MERCHANT_ID[:10]}...")
    
    if not settings.ZARINPAL_CALLBACK_URL:
        issues.append("❌ ZARINPAL_CALLBACK_URL is not set")
    else:
        print(f"✅ ZARINPAL_CALLBACK_URL is set: {settings.ZARINPAL_CALLBACK_URL}")
    
    if settings.ZARINPAL_SANDBOX:
        print("⚠️  ZARINPAL_SANDBOX is True (using sandbox mode)")
    else:
        print("✅ ZARINPAL_SANDBOX is False (using production mode)")
    
    if issues:
        print("\n⚠️  Issues found:")
        for issue in issues:
            print(f"  {issue}")
        return False
    return True


async def test_telegram_bot():
    """تست اتصال به Telegram Bot"""
    print("\n🔍 Testing Telegram Bot Connection...")
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username} ({me.first_name})")
        await bot.session.close()
        return True
    except Exception as e:
        print(f"❌ Telegram Bot error: {e}")
        return False


async def main():
    """اجرای تمام تست‌ها"""
    print("=" * 50)
    print("🧪 Webhook Setup Test")
    print("=" * 50)
    
    results = []
    
    # Test 1: Configuration
    results.append(("Configuration", test_config()))
    
    # Test 2: Health Endpoint
    results.append(("Health Endpoint", await test_health()))
    
    # Test 3: Callback Endpoint
    results.append(("Callback Endpoint", await test_callback()))
    
    # Test 4: Telegram Bot
    results.append(("Telegram Bot", await test_telegram_bot()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! System is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

