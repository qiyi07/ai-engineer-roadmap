from sqlmodel import Session, select, SQLModel
from src.models.db_models import Message
from src.core.config import settings
from sqlalchemy import create_engine

# 根据 DATABASE_URL 创建引擎（SQLite 不需要额外驱动）
engine = create_engine(settings.database_url, echo=False)

def get_session():
    """依赖注入用的 Session 生成器（后面会用到）"""
    with Session(engine) as session:
        yield session

class MessageRepository:
    @staticmethod
    def save(user_id: int, message: str, reply: str, temperature: float = 0.7) -> dict:
        with Session(engine) as session:
            db_msg = Message(
                user_id=user_id,
                message=message,
                reply=reply,
                temperature=temperature,
                tokens_used=len(message.split()) * 2  # 模拟 token
            )
            session.add(db_msg)
            session.commit()
            session.refresh(db_msg)  # 刷新获取自增 ID
            # 转换为字典返回（兼容原来的 Service 代码）
            return {
                "id": db_msg.id,
                "user_id": db_msg.user_id,
                "message": db_msg.message,
                "reply": db_msg.reply,
                "created_at": db_msg.created_at.isoformat(),
                "tokens_used": db_msg.tokens_used
            }

    @staticmethod
    def get_by_user(user_id: int, limit: int = 10) -> list:
        with Session(engine) as session:
            statement = select(Message).where(Message.user_id == user_id).order_by(Message.created_at.desc()).limit(limit)
            results = session.exec(statement).all()
            return [
                {
                    "id": msg.id,
                    "message": msg.message,
                    "reply": msg.reply,
                    "created_at": msg.created_at.isoformat(),
                    "tokens_used": msg.tokens_used
                }
                for msg in results
            ]