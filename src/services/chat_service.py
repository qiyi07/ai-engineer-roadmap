# from src.repositories.memory_db import MessageRepository
from src.repositories.message_repo import MessageRepository
from src.core.config import settings

class ChatService:
    """AI 对话业务逻辑"""
    
    @staticmethod
    def process_message(user_id: int, message: str, temperature: float = 0.7) -> dict:
        """处理用户消息，保存记录，返回回复"""
        # 1. 业务逻辑：模拟 AI 回复（未来换成真实 LLM 调用）
        # 可以读取 settings 来切换模型，比如使用 config 中的模型名称
        reply_text = f"[{settings.app_name}] 你说: '{message}'，温度={temperature}"
        
        # 2. 保存到数据库（Repository）
        record = MessageRepository.save(user_id, message, reply_text)
        
        # 3. 返回结果
        return {
            "reply": reply_text,
            "timestamp": record["created_at"],
            "tokens_used": len(message.split()) * 2,
            "record_id": record["id"]
        }
    
    @staticmethod
    def get_history(user_id: int, limit: int = 10) -> list:
        """获取用户历史"""
        return MessageRepository.get_by_user(user_id, limit)