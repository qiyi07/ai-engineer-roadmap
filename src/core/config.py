from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置类，自动从 .env 和环境变量加载"""

    app_name: str = Field(..., alias="APP_NAME")
    app_version: str = Field(..., alias="APP_VERSION")
    debug: bool = Field(True, alias="DEBUG")

    database_url: str = Field(..., alias="DATABASE_URL")

    # DeepSeek（或 OpenAI）配置
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")  # 改为必填
    openai_base_url: str = Field(
        default="https://api.deepseek.com/v1",
        alias="OPENAI_BASE_URL"
    )
    openai_model: str = Field(
        default="deepseek-chat",
        alias="OPENAI_MODEL"
    )
    system_prompt: str = Field(
        default="You are a helpful AI assistant.",
        alias="SYSTEM_PROMPT"
    )

    secret_key: str = Field(..., alias="SECRET_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings()
