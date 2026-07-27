from fastapi import APIRouter, Depends, Query, Path
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from sqlmodel import Session

from src.api.dependencies import get_current_user, get_db
from src.services.chat_service import ChatService

# ---------- 创建路由实例（必须！） ----------
router = APIRouter(prefix="/api/v1", tags=["AI服务"])

# ---------- 请求/响应模型 ----------
class ChatRequest(BaseModel):
    message: str
    temperature: float = 0.7

class ChatResponse(BaseModel):
    reply: str
    timestamp: datetime
    tokens_used: Optional[int] = None
    record_id: int

# ---------- 1. POST 对话 ----------
@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """处理对话，自动记录用户身份"""
    result = ChatService.process_message(
        session=db,
        user_id=current_user["id"],
        message=request.message,
        temperature=request.temperature
    )
    return ChatResponse(
        reply=result["reply"],
        timestamp=datetime.fromisoformat(result["created_at"]),
        tokens_used=result["tokens_used"],
        record_id=result["id"]
    )

# ---------- 2. GET 历史 ----------
@router.get("/users/history")
def get_history(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取当前用户的历史记录"""
    history = ChatService.get_history(db, current_user["id"], limit)
    return {
        "user_id": current_user["id"],
        "limit": limit,
        "history": history
    }

# ---------- 3. GET 配置信息 ----------
@router.get("/info")
def get_app_info():
    from src.core.config import settings
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }

# ---------- 4. GET 健康检查 ----------
@router.get("/health")
def health_check():
    return {"status": "ok", "version": "v1"}