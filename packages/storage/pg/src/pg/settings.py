from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_PG_", extra="ignore")

    host: str
    port: int = 5432
    username: str
    password: str
    db: str

    @property
    def pg_url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
