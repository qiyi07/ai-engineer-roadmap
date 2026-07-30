from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    """聊天消息表"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # 关联用户ID，加索引加速查询
    message: str
    reply: str
    temperature: float = 0.7
    tokens_used: int = 0
    created_at: datetime = Field(default_factory=datetime.now)


class User(SQLModel, table=True):
    """用户表（支持JWT认证）"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field(nullable=False)  # bcrypt哈希密文
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
