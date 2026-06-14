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

    # Cloudflare R2 (bỏ trống để dùng local storage)
    r2_account_id:       str | None = Field(default=None, validation_alias="R2_ACCOUNT_ID")
    r2_access_key_id:    str | None = Field(default=None, validation_alias="R2_ACCESS_KEY_ID")
    r2_secret_access_key: str | None = Field(default=None, validation_alias="R2_SECRET_ACCESS_KEY")
    r2_bucket_name:      str | None = Field(default=None, validation_alias="R2_BUCKET_NAME")
    r2_public_url:       str | None = Field(default=None, validation_alias="R2_PUBLIC_URL")  # https://pub-xxx.r2.dev hoặc custom domain

    @computed_field
    @property
    def use_r2(self) -> bool:
        return bool(self.r2_account_id and self.r2_access_key_id and
                    self.r2_secret_access_key and self.r2_bucket_name and self.r2_public_url)

    @computed_field
    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
