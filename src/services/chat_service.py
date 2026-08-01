from src.repositories.message_repo import MessageRepository
from src.services.llm_service import chat_with_llm_complete
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List

class ChatService:
    @staticmethod
    async def process_message(
        session,
        user_id: int,
        message: str,
        temperature: float = 0.7,
        history_limit: int = 5,  # 取最近 N 轮对话作为上下文
    ) -> dict:
        # 1. 从数据库获取该用户的最近对话（不包括本轮）
        recent = MessageRepository.get_by_user(session, user_id, limit=history_limit * 2)  # 每条记录包含一问一答
        # 按时间正序，并构造消息列表
        history_msgs: List[BaseMessage] = []
        for msg in reversed(recent):  # 已按时间倒序，反转为正序
            history_msgs.append(HumanMessage(content=msg["message"]))
            history_msgs.append(AIMessage(content=msg["reply"]))
        # 如果超过限制，截断（但 get_by_user 已经限制了总数）

        # 2. 调用 LLM，传入历史
        reply = await chat_with_llm_complete(
            user_message=message,
            history=history_msgs,
            temperature=temperature,
        )

        # 3. 保存新消息（此时 Repository 会自动记录）
        result = MessageRepository.save(session, user_id, message, reply, temperature)
        return result

    @staticmethod
    async def get_history(session, user_id: int, limit: int = 10) -> list:
        return MessageRepository.get_by_user(session, user_id, limit)
