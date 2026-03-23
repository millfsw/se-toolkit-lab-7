"""
Configuration management for the bot.

Loads settings from .env.bot.secret using pydantic-settings.
This provides type safety and validation for all configuration values.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Path to the .env.bot.secret file (in the project root, one level up from bot/)
_BASE_DIR = Path(__file__).parent.parent
_ENV_FILE = _BASE_DIR / ".env.bot.secret"


class BotSettings(BaseSettings):
    """Bot configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram bot token
    bot_token: str = ""

    # LMS API configuration
    lms_api_base_url: str = "http://localhost:42002"
    lms_api_key: str = ""

    # LLM API configuration
    llm_api_key: str = ""
    llm_api_base_url: str = ""
    llm_api_model: str = "coder-model"


# Global settings instance
settings = BotSettings()
