import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================
# CARREGA ENV ANTES DO PYDANTIC
# =============================

# define ambiente atual (dev/test/prod)
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")

env_file = BASE_DIR / f".env.{ENVIRONMENT}"

if env_file.exists():
    load_dotenv(env_file)
else:
    default_env = BASE_DIR / ".env"
    if default_env.exists():
        load_dotenv(default_env)


class Settings(BaseSettings):
    environment: str = ENVIRONMENT

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8"
    )

    def model_post_init(self, __context):
        if self.environment == "dev":
            self.database_url = "sqlite+aiosqlite:///./db_dev.sqlite"

        elif self.environment == "test":
            self.database_url = "sqlite+aiosqlite:///./db_test.sqlite"

        elif self.environment == "prod":
            if not self.database_url:
                raise ValueError("DATABASE_URL obrigatória em produção")

        if not self.database_url:
            raise ValueError("DATABASE_URL não configurada corretamente")

        print("ENV:", self.environment)
        print("DB:", self.database_url)


settings = Settings()