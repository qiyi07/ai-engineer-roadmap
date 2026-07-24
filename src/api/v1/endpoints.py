from fastapi import APIRouter, Query, Path
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 创建路由实例（后续在 main 中挂载）
router = APIRouter(prefix="/api/v1", tags=["AI服务"])

# ---------- 请求体模型 ----------
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[int] = None
    temperature: float = 0.7

class ChatResponse(BaseModel):
    reply: str
    timestamp: datetime
    tokens_used: Optional[int] = None

# ---------- 1. GET：路径参数 + 查询参数 ----------
@router.get("/users/{user_id}/history")
def get_user_history(
    user_id: int = Path(..., description="用户ID"),
    limit: int = Query(10, ge=1, le=100, description="返回条数"),
    keyword: Optional[str] = Query(None, description="关键词过滤")
):
    """演示路径参数 + 查询参数组合"""
    return {
        "user_id": user_id,
        "limit": limit,
        "keyword": keyword,
        "messages": [f"历史消息 {i}" for i in range(limit)],
        "timestamp": datetime.now().isoformat()
    }

# ---------- 2. POST：JSON 请求体 ----------
@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """演示 Pydantic 请求体 + 响应模型"""
    # 模拟 AI 回复（W3 接入真实 LLM）
    reply_text = f"你说: '{request.message}'。这是模拟回复 (温度={request.temperature})"
    
    return ChatResponse(
        reply=reply_text,
        timestamp=datetime.now(),
        tokens_used=len(request.message.split()) * 2  # 模拟 token 计算
    )

# ---------- 3. GET：简单查询 ----------
@router.get("/health")
def api_health():
    return {"status": "ok", "version": "v1"}