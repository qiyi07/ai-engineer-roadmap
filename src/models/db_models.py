from datetime import datetime
from typing import Optional, List

from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    """用户表（支持JWT认证）"""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # 关系（可选，方便ORM查询）
    sessions: List["ChatSession"] = Relationship(back_populates="user")


class ChatSession(SQLModel, table=True):
    """对话会话表，一个用户可有多个会话"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(default="新对话", max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # 关系
    user: "User" = Relationship(back_populates="sessions")
    messages: List["Message"] = Relationship(back_populates="session")


class Message(SQLModel, table=True):
    """聊天消息表，关联到具体会话"""
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(foreign_key="chatsession.id", index=True)  # 关联会话
    user_id: int = Field(index=True)  # 冗余字段，加速查询（也可通过session关联）
    message: str
    reply: str
    temperature: float = 0.7
    tokens_used: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

    # 关系
    session: "ChatSession" = Relationship(back_populates="messages")
