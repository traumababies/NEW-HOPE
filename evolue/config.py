"""Application settings.

Loaded from environment / .env file. No secrets are committed; the repo ships
.env.example only.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Reads .env keys directly (no prefix). Field aliases map the owner's
    # actual key names (OWNER_EMAIL / OWNER_PASSWORD) onto our settings fields.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
        case_sensitive=False,
    )

    app_name: str = "Évolué Media Team"
    app_env: str = "development"  # development | production

    # Authorisation -------------------------------------------------------
    # validate_as so OWNER_EMAIL maps onto admin_email:
    admin_email: str = Field(default="", validation_alias="OWNER_EMAIL")
    session_secret: str = Field(default="", validation_alias="SESSION_SECRET")
    owner_password: str = Field(default="", validation_alias="OWNER_PASSWORD")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",  # read keys as-is (OWNER_EMAIL -> OWNER_EMAIL)
        case_sensitive=False,
    )

    # Azure SQL -----------------------------------------------------------
    sql_server: str = ""
    sql_database: str = ""
    sql_username: str = ""
    sql_password: str = ""
    sql_conn_str: str = ""  # overrides the four above when non-empty
    # Full URL form from .env, e.g.
    #   mssql+pyodbc://USER:PWD@SERVER:1433/DB?driver=ODBC+Driver+18+for+SQL+Server
    database_url: str = Field(default="", validation_alias="DATABASE_URL")

    # Azure Blob storage --------------------------------------------------
    azure_blob_account: str = "godzilla1126"
    azure_blob_key: str = ""
    azure_blob_conn_str: str = ""
    azure_storage_account_url: str = ""          # from .env AZURE_STORAGE_ACCOUNT_URL
    azure_storage_connection_string: str = ""    # from .env AZURE_STORAGE_CONNECTION_STRING
    azure_storage_container: str = "bunbuns"     # from .env AZURE_STORAGE_CONTAINER
    azure_storage_container_ephemera: str = "ephemera"

    # Containers (the three distinct roles from the spec) ------------------
    container_bunbuns: str = "bunbuns"      # permanent Library
    container_ephemera: str = "ephemera"    # scout quarantine
    container_scrappa: str = "magic-carpet" # pipeline scratchpad (owner-named)
    # AI (local Ollama) ----------------------------------------------------
    ollama_enabled: bool = False
    ollama_endpoint: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:3b"
    ollama_vision_model: str = ""

    # Azure AI Vision (Cataloger eyes; scout triage) -------------------------
    azure_vision_endpoint: str = Field(default="", validation_alias="AZURE_VISION_ENDPOINT")
    azure_vision_api_key: str = Field(default="", validation_alias="AZURE_VISION_API_KEY")
    azure_vision_key: str = ""                       # alternate spelling

    # Groq (Current Events / Fact Check) ------------------------------------
    groq_api_key: str = ""
    groq_model: str = ""
    groq_fact_model: str = ""

    # DeepSeek (Creative Director, Muse, Creative Grader, Cataloger, Copywriter)
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # OpenRouter (fallback for all roles) ------------------------------------
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    openrouter_model: str = "anthropic/claude-sonnet-4"

    # Providers for the four Content Scouts (from The Library / B.8) --------
    pexels_api_key: str = ""
    pixabay_api_key: str = ""
    unsplash_access_key: str = ""
    coverr_api_key: str = ""

    # Scout per-platform limits (owner-specified, not guessed) --------------
    scout_pixabay_per_page: int = 200
    scout_pexels_per_page: int = 80
    scout_unsplash_per_page: int = 30
    scout_unsplash_sleep_s: float = 12.0
    scout_coverr_page_size: int = 20
    scout_coverr_sleep_s: float = 12.0

    # Production rules ------------------------------------------------------
    max_redo_attempts: int = 2
    timezone: str = "America/Phoenix"

    # JAN override passwords (per phase; owner-set, never committed) ---------
    jan_override_creative_brief: str = ""
    jan_override_muse: str = ""
    jan_override_scout: str = ""
    jan_override_catalog: str = ""
    jan_override_media_editor: str = ""
    jan_override_copywriter: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
