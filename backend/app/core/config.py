from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    gemini_api_key: str = ""

    openai_model: str = "gpt-4o-mini"
    anthropic_model: str = "claude-3-5-haiku-latest"
    gemini_model: str = "gemini-1.5-flash"
    judge_model: str = "gpt-4o-mini"

    frontend_origin: str = "http://localhost:3000"


settings = Settings()
