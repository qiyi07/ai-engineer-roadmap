from src.repositories.message_repo import MessageRepository
from src.services.llm_service import chat_with_llm_complete

class ChatService:
    @staticmethod
    async def process_message(
        session,
        user_id: int,
        message: str,
        temperature: float = 0.7,
    ) -> dict:
        reply = await chat_with_llm_complete(
            user_message=message,
            temperature=temperature,
        )
        result = MessageRepository.save(session, user_id, message, reply, temperature)
        return result

    @staticmethod
    async def get_history(session, user_id: int, limit: int = 10) -> list:
        return MessageRepository.get_by_user(session, user_id, limit)
