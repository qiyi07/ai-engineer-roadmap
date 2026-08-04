from sqlmodel import Session, select
from src.models.db_models import ChatSession
from typing import List, Optional
from datetime import datetime

class SessionRepository:
    @staticmethod
    def create(session: Session, user_id: int, title: str = "新对话") -> ChatSession:
        chat_session = ChatSession(user_id=user_id, title=title)
        session.add(chat_session)
        session.commit()
        session.refresh(chat_session)
        return chat_session

    @staticmethod
    def get_by_user(session: Session, user_id: int) -> List[ChatSession]:
        stmt = select(ChatSession).where(ChatSession.user_id == user_id).order_by(ChatSession.updated_at.desc())
        return session.exec(stmt).all()

    @staticmethod
    def get_by_id(session: Session, session_id: int, user_id: int) -> Optional[ChatSession]:
        stmt = select(ChatSession).where(
            ChatSession.id == session_id,
            ChatSession.user_id == user_id
        )
        return session.exec(stmt).first()

    @staticmethod
    def update_title(session: Session, session_id: int, user_id: int, title: str) -> Optional[ChatSession]:
        chat_session = SessionRepository.get_by_id(session, session_id, user_id)
        if chat_session:
            chat_session.title = title
            chat_session.updated_at = datetime.now()
            session.commit()
            session.refresh(chat_session)
        return chat_session

    @staticmethod
    def delete(session: Session, session_id: int, user_id: int) -> bool:
        chat_session = SessionRepository.get_by_id(session, session_id, user_id)
        if chat_session:
            session.delete(chat_session)
            session.commit()
            return True
        return False