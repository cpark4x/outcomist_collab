"""Application configuration."""

from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Keys
    anthropic_api_key: str

    # Database
    database_url: str = "sqlite+aiosqlite:///./data/database.sqlite"

    # Storage
    data_dir: Path = Path("./data/projects")

    # CORS
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    # Claude API
    claude_model: str = "claude-3-7-sonnet-20250219"
    claude_max_tokens: int = 4096
    claude_temperature: float = 1.0

    def __init__(self, **kwargs):
        """Initialize settings and ensure data directory exists."""
        super().__init__(**kwargs)
        self.data_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance."""
    return settings
