from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # When set (e.g. in Docker), connection details are taken from this in database.py —
    # pydantic-settings re-applies env after @model_validator, so we parse the URL there.
    database_url: str | None = Field(default=None, validation_alias="DATABASE_URL")

    db_host: str = Field(default="localhost")
    db_port: int = Field(default=5432)
    db_name: str = Field(default="huyvo_db")
    db_user: str = Field(default="huyvo")
    db_password: str = Field(default="huyvo_secret")

    secret_key: str = Field(default="change-me-in-production-very-long-secret", validation_alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60 * 24 * 7, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")

    debug: bool = Field(default=False, validation_alias="DEBUG")
    allowed_origins: str = Field(
        default="http://localhost:5173,http://localhost:3000,http://localhost",
        validation_alias="ALLOWED_ORIGINS",
    )
    media_dir: str = Field(default="./media", validation_alias="MEDIA_DIR")

    @computed_field
    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
