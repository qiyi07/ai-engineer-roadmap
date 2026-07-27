from src.repositories.message_repo import MessageRepository

class ChatService:
    @staticmethod
    def process_message(session, user_id: int, message: str, temperature: float = 0.7) -> dict:
        # 将 session 透传给 Repository
        return MessageRepository.save(session, user_id, message, temperature)
    
    @staticmethod
    def get_history(session, user_id: int, limit: int = 10) -> list:
        return MessageRepository.get_by_user(session, user_id, limit)