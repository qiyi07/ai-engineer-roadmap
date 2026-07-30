from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类，自动从 .env 和环境变量加载"""

    app_name: str = Field(..., alias="APP_NAME")
    app_version: str = Field(..., alias="APP_VERSION")
    debug: bool = Field(True, alias="DEBUG")

    database_url: str = Field(..., alias="DATABASE_URL")
    openai_api_key: str = Field("", alias="OPENAI_API_KEY")
    secret_key: str = Field(..., alias="SECRET_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"  # 强制 UTF-8 编码，避免 Windows 下的解码错误
        case_sensitive = False  # 不区分大小写


# 创建单例配置对象（整个项目只加载一次）
settings = Settings()
