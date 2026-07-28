from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from sqlmodel import Session

from src.core.config import settings, Settings
from src.core.security import decode_access_token
from src.repositories.message_repo import engine


def get_settings() -> Settings:
    """
    依赖项：返回应用配置对象。
    """
    return settings


def get_db():
    """
    依赖项：提供数据库会话（Session）。
    每个请求创建一个新的 Session，请求结束后自动关闭。
    """
    with Session(engine) as session:
        yield session


async def get_current_user(
    token: Optional[str] = Header(None, alias="Authorization")
) -> dict:
    """
    依赖项：从 Authorization 头提取 JWT 令牌，验证并返回用户信息。
    格式要求：Authorization: Bearer <token>
    如果令牌缺失或无效，抛出 401 异常。
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 移除 "Bearer " 前缀（如果有）
    if token.startswith("Bearer "):
        token = token[7:]

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identifier",
        )

    # 可在此处从数据库查询用户状态（如是否禁用），增强安全性
    return {
        "id": int(user_id),
        "username": payload.get("username", "unknown")
    }