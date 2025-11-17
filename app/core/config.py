from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str | None = None
    DATABASE_URL: str = "sqlite:///./gym_bot.db"
    ZARINPAL_MERCHANT_ID: str | None = None
    ZARINPAL_CALLBACK_URL: str | None = None
    ZARINPAL_SANDBOX: bool = True
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "change_me"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

