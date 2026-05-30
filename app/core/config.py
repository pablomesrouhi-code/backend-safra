from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite:///./safraskin.db"
    CORS_ORIGINS: str = (
        "http://localhost:3000,https://safraskin.online,https://www.safraskin.online"
    )

    GOOGLE_SHEETS_WEBHOOK_URL: str = ""
    GOOGLE_SHEETS_SECRET: str = ""

    META_PIXEL_ID: str = ""
    META_ACCESS_TOKEN: str = ""
    META_TEST_EVENT_CODE: str = ""

    TIKTOK_PIXEL_ID: str = ""
    TIKTOK_ACCESS_TOKEN: str = ""

    SNAP_PIXEL_ID: str = ""
    SNAP_ACCESS_TOKEN: str = ""

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    ORDER_NUMBER_PREFIX: str = "SS"
    UPSELL_PRICE_SAR: int = 99

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def sheets_enabled(self) -> bool:
        return bool(self.GOOGLE_SHEETS_WEBHOOK_URL.strip())

    @property
    def meta_capi_enabled(self) -> bool:
        return bool(self.META_PIXEL_ID and self.META_ACCESS_TOKEN)

    @property
    def tiktok_capi_enabled(self) -> bool:
        return bool(self.TIKTOK_PIXEL_ID and self.TIKTOK_ACCESS_TOKEN)

    @property
    def snap_capi_enabled(self) -> bool:
        return bool(self.SNAP_PIXEL_ID and self.SNAP_ACCESS_TOKEN)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
