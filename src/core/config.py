from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """应用配置类，自动从 .env 和环境变量加载"""
    app_name: str = Field(..., alias="APP_NAME")
    app_version: str = Field(..., alias="APP_VERSION")
    debug: bool = Field(True, alias="DEBUG")
    
    database_url: str = Field(..., alias="DATABASE_URL")
    openai_api_key: str = Field("", alias="OPENAI_API_KEY")  # 默认空，避免报错
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # 允许不区分大小写

# 创建单例配置对象（整个项目只加载一次）
settings = Settings()