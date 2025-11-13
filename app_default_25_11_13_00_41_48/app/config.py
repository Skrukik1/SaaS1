from pydantic import BaseSettings, AnyHttpUrl, validator
from typing import List, Optional


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600

    # OAuth2
    OAUTH2_CLIENT_ID: str
    OAUTH2_CLIENT_SECRET: str
    OAUTH2_AUTHORIZATION_URL: AnyHttpUrl
    OAUTH2_TOKEN_URL: AnyHttpUrl
    OAUTH2_USERINFO_URL: AnyHttpUrl
    OAUTH2_REDIRECT_URL: AnyHttpUrl

    # Rate limiter
    RATE_LIMIT_DEFAULT: str = "100/minute"
    RATE_LIMIT_ADMIN: str = "1000/minute"

    # Logging
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str]

    # Monitoring
    PROMETHEUS_METRICS_PATH: str = "/metrics"
    PROMETHEUS_SCRAPE_INTERVAL: str = "15s"

    # Discord bot
    DISCORD_BOT_TOKEN: str
    DISCORD_COMMAND_PREFIX: str = "!"
    DISCORD_SPAM_PROTECTION_ENABLED: bool = True
    DISCORD_COMMAND_COOLDOWN_SECONDS: int = 5

    # CORS
    CORS_ORIGINS: Optional[List[AnyHttpUrl]] = None

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
