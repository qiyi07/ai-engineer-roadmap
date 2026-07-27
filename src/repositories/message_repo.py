from sqlmodel import Session, select
from src.models.db_models import Message
from src.core.config import settings
from sqlalchemy import create_engine

# 引擎创建保持不变（不再每次创建 Session）
engine = create_engine(
    settings.database_url,
    echo=False,
    # PostgreSQL 不需要 check_same_thread
)



class MessageRepository:
    @staticmethod
    def save(session: Session, user_id: int, message: str, reply: str, temperature: float = 0.7) -> dict:
        """接收外部传入的 session，由 FastAPI 管理生命周期"""
        db_msg = Message(
            user_id=user_id,
            message=message,
            reply=reply,
            temperature=temperature,
            tokens_used=len(message.split()) * 2
        )
        session.add(db_msg)
        session.commit()
        session.refresh(db_msg)
        return {
            "id": db_msg.id,
            "user_id": db_msg.user_id,
            "message": db_msg.message,
            "reply": db_msg.reply,
            "created_at": db_msg.created_at.isoformat(),
            "tokens_used": db_msg.tokens_used
        }

    @staticmethod
    def get_by_user(session: Session, user_id: int, limit: int = 10) -> list:
        """接收外部传入的 session"""
        statement = (
            select(Message)
            .where(Message.user_id == user_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
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