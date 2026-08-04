from sqlalchemy import create_engine
from sqlmodel import Session, select
from datetime import datetime

from src.core.config import settings
from src.models.db_models import Message, ChatSession
engine = create_engine(
    settings.database_url,
    echo=False,
    # PostgreSQL 不需要 check_same_thread
)


class MessageRepository:
    @staticmethod
    def save(
        session: Session,
        session_id: int,
        user_id: int,
        message: str,
        reply: str,
        temperature: float = 0.7,
    ) -> dict:
        """保存消息，关联到指定会话"""
        db_msg = Message(
            session_id=session_id,
            user_id=user_id,
            message=message,
            reply=reply,
            temperature=temperature,
            tokens_used=len(message.split()) * 2,
        )
        session.add(db_msg)
        session.commit()
        session.refresh(db_msg)

        # 更新对应会话的 updated_at
        chat_session = session.get(ChatSession, session_id)
        if chat_session:
            chat_session.updated_at = datetime.now()
            session.commit()

        return {
            "id": db_msg.id,
            "session_id": db_msg.session_id,
            "user_id": db_msg.user_id,
            "message": db_msg.message,
            "reply": db_msg.reply,
            "created_at": db_msg.created_at.isoformat(),
            "tokens_used": db_msg.tokens_used,
        }

    @staticmethod
    def get_by_user(session: Session, user_id: int, limit: int = 10) -> list:
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
                "session_id": msg.session_id,
                "message": msg.message,
                "reply": msg.reply,
                "created_at": msg.created_at.isoformat(),
                "tokens_used": msg.tokens_used,
            }
            for msg in results
        ]

    @staticmethod
    def get_by_session(session: Session, session_id: int, limit: int = 20) -> list:
        """按会话 ID 获取消息历史（正序，用于上下文）"""
        statement = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.asc())   # 正序，最早的消息在前
            .limit(limit)
        )
        results = session.exec(statement).all()
        return [
            {
                "id": msg.id,
                "message": msg.message,
                "reply": msg.reply,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in results
        ]