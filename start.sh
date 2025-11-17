#!/bin/bash
# اسکریپت اجرای همزمان FastAPI و Telegram Bot
# برای Railway یا Render

# اجرای FastAPI در background
uvicorn app.web_admin.main:app --host 0.0.0.0 --port ${PORT:-8000} &

# اجرای Telegram Bot
python -m app.telegram.main &

# نگه داشتن container زنده
wait

