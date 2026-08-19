from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Coffee House API"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str = "coffee_user"
    database_password: str = "coffee_password"
    database_name: str = "coffee_house"

    payment_webhook_secret: str

    cors_origins: str = (
        "http://localhost:5174,"
        "http://127.0.0.1:5174"
    )

    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}"
            f"/{self.database_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()