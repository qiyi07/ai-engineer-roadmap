from fastapi import APIRouter, Depends, Query, Path
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# 导入依赖和 Service
from src.api.dependencies import get_current_user, get_settings
from src.core.config import Settings
from src.services.chat_service import ChatService

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
    settings: Settings = Depends(get_settings),      # 注入配置
    current_user: dict = Depends(get_current_user)   # 注入用户
):
    """处理对话，自动记录用户身份"""
    # 调用 Service
    result = ChatService.process_message(
        user_id=current_user["id"],
        message=request.message,
        temperature=request.temperature
    )
    
    # 返回响应（符合 ChatResponse 模型）
    return ChatResponse(
        reply=result["reply"],
        timestamp=datetime.fromisoformat(result["timestamp"]),
        tokens_used=result["tokens_used"],
        record_id=result["record_id"]
    )

# ---------- 2. GET 历史 ----------
@router.get("/users/history")
def get_history(
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """获取当前用户的历史记录"""
    history = ChatService.get_history(current_user["id"], limit)
    return {
        "user_id": current_user["id"],
        "limit": limit,
        "history": history
    }

# ---------- 3. GET 配置信息（演示注入 settings） ----------
@router.get("/info")
def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }