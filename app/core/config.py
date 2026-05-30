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

    # MaxMind GeoLite2 (optional — CAPI country + optional KSA-only orders)
    MAXMIND_ACCOUNT_ID: str = ""
    MAXMIND_LICENSE_KEY: str = ""
    MAXMIND_GEOIP_DB_PATH: str = "./data/GeoLite2-Country.mmdb"
    GEOIP_ENFORCE_KSA: bool = False

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

    @property
    def maxmind_enabled(self) -> bool:
        return bool(self.MAXMIND_LICENSE_KEY.strip()) or self.geoip_db_path_resolved.is_file()

    @property
    def geoip_db_path_resolved(self):
        from pathlib import Path

        return Path(self.MAXMIND_GEOIP_DB_PATH)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
