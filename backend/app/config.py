from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # App
    APP_NAME: str = "Eko AI Business Automation"
    APP_VERSION: str = "0.5.1"
    APP_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://eko:eko_dev_pass@localhost:5432/eko_ai"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # API Keys
    # AI Provider (openai, kimi, or ollama)
    AI_PROVIDER: str = "kimi"

    # OpenAI settings
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # Kimi (Kimi Code API) settings
    KIMI_API_KEY: str = ""
    KIMI_BASE_URL: str = "https://api.kimi.com/coding/v1"
    KIMI_MODEL: str = "kimi-for-coding"
    KIMI_EMBEDDING_MODEL: str = "moonshot-v1-embedding-1024"

    # Ollama (local) settings
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434/v1"
    OLLAMA_MODEL: str = "qwen2.5-coder:14b"
    OLLAMA_EMBEDDING_MODEL: str = "nomic-embed-text"

    # MiniMax settings
    MINIMAX_API_KEY: str = ""
    MINIMAX_BASE_URL: str = "https://api.minimax.io/v1"
    MINIMAX_MODEL: str = "MiniMax-M2.7"
    MINIMAX_EMBEDDING_MODEL: str = "embedding-001"

    RESEND_API_KEY: str = ""
    RESEND_FROM_EMAIL: str = "Eko AI <contact@biz.ekoaiautomation.com>"
    RESEND_WEBHOOK_SECRET: str = ""
    RESEND_INBOUND_DOMAIN: str = "biz.ekoaiautomation.com"
    AUTO_CREATE_LEAD_FROM_INBOUND: bool = True
    AUTO_REPLY_ENABLED: bool = True

    OUTSCRAPER_API_KEY: str = ""
    APIFY_API_KEY: str = ""
    YELP_API_KEY: str = ""
    SERPAPI_API_KEY: str = ""

    # Phase 3: Voice
    RETELL_API_KEY: str = ""
    VAPI_API_KEY: str = "f361bb66-8274-403a-8c0c-b984d7dd1cee"
    VAPI_PHONE_NUMBER_ID: str = "81c18484-e0eb-4dd1-933c-a2a922427b07"
    VAPI_INBOUND_PHONE_NUMBER: str = "+1-256-364-1727"
    VAPI_BLACK_VOLT_ASSISTANT_ID: str = "b7bc5bc2-5e54-4e40-8cf9-63a06f478aa3"
    VAPI_EKO_ASSISTANT_ID: str = "8c2de53b-3979-4e15-8824-757b749b27c3"

    # Phase 2: Calendar
    CAL_COM_API_KEY: str = ""
    CAL_COM_USERNAME: str = "eko-ai"

    # Phase 4: Payments
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    STRIPE_PRICE_STARTER: str = ""
    STRIPE_PRICE_GROWTH: str = ""
    STRIPE_PRICE_ENTERPRISE: str = ""

    # Compliance
    DNC_SYNC_CRON: str = "0 2 1 * *"
    MAX_CONTACT_ATTEMPTS: int = 5
    COOLDOWN_HOURS_BETWEEN_CONTACTS: int = 72

    # Frontend URL for proposal links
    FRONTEND_URL: str = "http://localhost:3001"

    # Notifications
    ENDER_NOTIFICATION_EMAIL: str = "ender@ekoaiautomation.com"

    # Eko Rog Telegram Notifications
    TELEGRAM_BOT_TOKEN: str = "8264195169:AAG94XS7lPHh_L7DBvTNVKSR_4geB_WEju0"
    TELEGRAM_CHAT_ID: str = "771213858"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://localhost:8000"

    # Paperclip — AI Company Control Plane
    PAPERCLIP_API_URL: str = "http://100.88.47.99:3100"
    PAPERCLIP_COMPANY_ID: str = "a5151f95-51cd-4d2d-a35b-7d7cb4f4102e"
    PAPERCLIP_API_KEY: str = ""

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
