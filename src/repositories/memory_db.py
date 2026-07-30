from datetime import datetime
from typing import Dict, List

# 模拟数据库表：存储聊天记录
_messages: List[Dict] = []
_counter = 0


class MessageRepository:
    """负责消息的增删改查（目前是内存存储）"""

    @staticmethod
    def save(user_id: int, message: str, reply: str) -> Dict:
        global _counter
        _counter += 1
        record = {
            "id": _counter,
            "user_id": user_id,
            "message": message,
            "reply": reply,
            "created_at": datetime.now().isoformat(),
        }
        _messages.append(record)
        return record

    @staticmethod
    def get_by_user(user_id: int, limit: int = 10) -> List[Dict]:
        """按用户 ID 查询历史记录（倒序返回最新）"""
        result = [m for m in _messages if m["user_id"] == user_id]
        return result[-limit:]  # 取最近的 limit 条
