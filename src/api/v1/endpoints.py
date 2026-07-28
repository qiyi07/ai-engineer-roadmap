from fastapi import APIRouter, Depends, Query, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from sqlmodel import Session

from src.api.dependencies import get_current_user, get_db
from src.services.chat_service import ChatService
from src.repositories.user_repo import UserRepository
from src.core.security import create_access_token

# ---------- 路由实例 ----------
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

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- 1. 注册 ----------
@router.post("/register", response_model=TokenResponse)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """用户注册，成功后直接返回 JWT token"""
    # 检查用户名或邮箱是否已存在
    if UserRepository.get_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if UserRepository.get_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 创建用户
    user = UserRepository.create_user(
        db, user_data.username, user_data.email, user_data.password
    )
    
    # 签发 token
    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ---------- 2. 登录 ----------
@router.post("/login", response_model=TokenResponse)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """用户登录，返回 JWT token"""
    user = UserRepository.authenticate(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}

# ---------- 3. 对话（需要认证） ----------
@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   # 强制 JWT 认证
):
    """处理对话，自动关联当前登录用户"""
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

# ---------- 4. 历史记录（需要认证） ----------
@router.get("/users/history")
def get_history(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取当前用户的历史对话"""
    history = ChatService.get_history(db, current_user["id"], limit)
    return {
        "user_id": current_user["id"],
        "limit": limit,
        "history": history
    }

# ---------- 5. 应用信息（公开） ----------
@router.get("/info")
def get_app_info():
    from src.core.config import settings
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }

# ---------- 6. 健康检查（公开） ----------
@router.get("/health")
def health_check():
    return {"status": "ok", "version": "v1"}