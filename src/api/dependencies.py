from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from src.core.config import settings, Settings

# 依赖 1：注入配置对象（未来所有接口都能用）
def get_settings() -> Settings:
    return settings

# 依赖 2：模拟获取当前用户（未来换成 JWT 解析）
def get_current_user(
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    """从请求头 X-User-ID 中读取用户 ID，如果没有则返回默认用户"""
    if x_user_id is None:
        # 开发模式默认用户，生产环境应该抛出 401
        return {"id": 1, "name": "default_user"}
    
    # 简单校验：如果用户 ID 不是数字，抛出 401
    if not x_user_id.isdigit():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid User ID format"
        )
    return {"id": int(x_user_id), "name": f"user_{x_user_id}"}