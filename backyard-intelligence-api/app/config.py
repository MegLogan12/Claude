"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings."""

    service_name: str = "backyard-intelligence-api"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/backyard"

    google_geocoding_api_key: str = ""
    mapbox_api_token: str = ""
    arcgis_api_key: str = ""

    default_imagery_provider: str = "arcgis"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
