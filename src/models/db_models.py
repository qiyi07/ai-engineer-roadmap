from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

# 这个类会被 Alembic 检测到，自动创建表
class Message(SQLModel, table=True):
    """聊天消息表，对应 SQLite 的 message 表"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)  # 索引，便于按用户查询
    message: str
    reply: str
    temperature: float = 0.7
    tokens_used: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

    # 表名默认为类名小写，可以指定 __tablename__ = "messages"