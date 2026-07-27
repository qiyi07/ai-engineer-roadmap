# src/api/dependencies.py
from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from sqlmodel import Session

from src.core.config import settings, Settings
from src.repositories.message_repo import engine


def get_settings() -> Settings:
    """
    依赖项：返回应用配置对象。
    所有需要读取 .env 配置的接口都可以注入此依赖。
    """
    return settings


def get_current_user(
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
) -> dict:
    """
    依赖项：从请求头 X-User-ID 中获取当前用户信息。
    开发模式下，如果没有传递则返回默认用户（id=1）。
    生产环境应替换为真正的 JWT 解析逻辑。
    """
    if x_user_id is None:
        # 开发模式默认用户
        return {"id": 1, "name": "default_user"}

    # 简单校验：如果传递的不是纯数字，视为非法
    if not x_user_id.isdigit():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User ID format. Must be a number."
        )

    return {"id": int(x_user_id), "name": f"user_{x_user_id}"}


def get_db():
    """
    依赖项：提供数据库会话（Session）。
    每个请求会创建一个新的 Session，请求结束后自动关闭。
    配合 FastAPI 的 Depends，可以实现事务自动管理。
    """
    with Session(engine) as session:
        yield session