from sqlmodel import select
from src.repositories.message_repo import MessageRepository
from src.repositories.session_repo import SessionRepository
from src.services.llm_service import chat_with_llm_complete, generate_session_title
from src.models.db_models import Message
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List, Optional

class ChatService:
    @staticmethod
    async def process_message(
        session,
        user_id: int,
        session_id: int,
        message: str,
        temperature: float = 0.7,
        history_limit: int = 10,
    ) -> dict:
        # 检查是否是第一条消息（用于生成标题）
        existing = session.exec(
            select(Message).where(Message.session_id == session_id)
        ).all()
        is_first_message = len(existing) == 0

        # 获取该会话的历史消息（用于上下文）
        recent = MessageRepository.get_by_session(session, session_id, limit=history_limit * 2)
        history_msgs: List[BaseMessage] = []
        for msg in recent:
            history_msgs.append(HumanMessage(content=msg["message"]))
            history_msgs.append(AIMessage(content=msg["reply"]))

        # 调用 LLM
        reply = await chat_with_llm_complete(
            user_message=message,
            history=history_msgs,
            temperature=temperature,
        )

        # 保存消息（关联 session_id）
        result = MessageRepository.save(session, session_id, user_id, message, reply, temperature)

        # 如果是第一条消息，生成会话标题
        if is_first_message:
            title = await generate_session_title(message)
            SessionRepository.update_title(session, session_id, user_id, title)

        return result

    @staticmethod
    async def get_history(session, session_id: int, limit: int = 20) -> list:
        return MessageRepository.get_by_session(session, session_id, limit)

    @staticmethod
    async def get_or_create_default_session(session, user_id: int) -> int:
        sessions = SessionRepository.get_by_user(session, user_id)
        if sessions:
            return sessions[0].id
        new_session = SessionRepository.create(session, user_id)
        return new_session.id