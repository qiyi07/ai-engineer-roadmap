import random
import time
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session

from src.api.dependencies import get_current_user, get_db, verification_codes
from src.api.rate_limit import limiter
from src.core.security import create_access_token
from src.repositories.user_repo import UserRepository
from src.repositories.session_repo import SessionRepository
from src.services.chat_service import ChatService
from src.utils.email import send_verification_email
from src.services.llm_service import chat_with_llm_stream
from src.utils.logger import logger
from src.services.rag_service import rag_answer
from src.projects.resume_optimizer.service import parse_resume, analyze_jd, tailor_cv
from src.projects.resume_optimizer.schemas import Resume, MatchAnalysis, TailoredCVResponse

# ---------- 路由实例 ----------
router = APIRouter(prefix="/api/v1", tags=["AI服务"])


# ---------- 请求/响应模型 ----------
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None  #可选，不传则使用默认会话
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


class EmailRequest(BaseModel):
    email: str


class VerifyEmailRequest(BaseModel):
    email: str
    code: str


#会话管理模型
class SessionCreate(BaseModel):
    title: Optional[str] = "新对话"


class SessionResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

class RAGRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3
    temperature: Optional[float] = 0.3

class RAGResponse(BaseModel):
    answer: str
    sources: List[dict]
    has_answer: bool


class ResumeTextInput(BaseModel):
    text: str

class JDTextInput(BaseModel):
    text: str
    title: Optional[str] = None
    company: Optional[str] = None

class TailorRequest(BaseModel):
    resume_text: str
    jd_text: str
    style: Optional[str] = "professional"

# ---------- 1. 注册 ----------
@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """用户注册，成功后直接返回 JWT token"""
    if UserRepository.get_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if UserRepository.get_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user = UserRepository.create_user(db, user_data.username, user_data.email, user_data.password)
    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}


# ---------- 2. 登录 ----------
@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = UserRepository.authenticate(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}


# ---------- 3. 创建会话 ----------
@router.post("/sessions", response_model=SessionResponse)
def create_session(
    data: SessionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """创建新会话"""
    session = SessionRepository.create(db, current_user["id"], data.title)
    return SessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )


# ---------- 4. 列表会话 ----------
@router.get("/sessions", response_model=List[SessionResponse])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取当前用户的所有会话"""
    sessions = SessionRepository.get_by_user(db, current_user["id"])
    return [
        SessionResponse(
            id=s.id,
            title=s.title,
            created_at=s.created_at,
            updated_at=s.updated_at,
        )
        for s in sessions
    ]


# ---------- 5. 删除会话 ----------
@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """删除指定会话（会同时删除该会话下的所有消息）"""
    success = SessionRepository.delete(db, session_id, current_user["id"])
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted"}


# ---------- 6. 对话（非流式，保存历史） ----------
@router.post("/chat", response_model=ChatResponse)
@limiter.limit("5/minute")
async def chat_endpoint(
    request: Request,
    chat_req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """非流式对话，支持多会话。不传 session_id 时使用最近会话"""
    # 确定 session_id
    session_id = chat_req.session_id
    if session_id is None:
        session_id = await ChatService.get_or_create_default_session(db, current_user["id"])
    else:
        # 验证该会话属于当前用户
        sess = SessionRepository.get_by_id(db, session_id, current_user["id"])
        if not sess:
            raise HTTPException(status_code=404, detail="Session not found")

    # 异常捕获 + 日志记录
    try:
        result = await ChatService.process_message(
            session=db,
            user_id=current_user["id"],
            session_id=session_id,
            message=chat_req.message,
            temperature=chat_req.temperature,
        )
    except Exception as e:
        logger.error(f"对话处理失败: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="AI 服务暂时不可用")

    return ChatResponse(
        reply=result["reply"],
        timestamp=datetime.fromisoformat(result["created_at"]),
        tokens_used=result["tokens_used"],
        record_id=result["id"],
    )


# ---------- 7. 流式对话（不保存历史，仅演示） ----------
@router.post("/chat/stream")
@limiter.limit("5/minute")
async def chat_stream(
    request: Request,
    chat_req: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    """流式对话，返回 Server-Sent Events (SSE)，不保存历史"""
    async def generate():
        async for chunk in chat_with_llm_stream(
            user_message=chat_req.message,
            temperature=chat_req.temperature,
        ):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


# ---------- 8. 历史记录（按会话） ----------
@router.get("/users/history")
@limiter.limit("10/minute")
async def get_history(
    request: Request,
    session_id: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """获取指定会话的历史记录。不传 session_id 时使用最近会话"""
    if session_id is None:
        sessions = SessionRepository.get_by_user(db, current_user["id"])
        if not sessions:
            return {"session_id": None, "limit": limit, "history": []}
        session_id = sessions[0].id
    else:
        sess = SessionRepository.get_by_id(db, session_id, current_user["id"])
        if not sess:
            raise HTTPException(status_code=404, detail="Session not found")

    history = await ChatService.get_history(db, session_id, limit)
    return {"session_id": session_id, "limit": limit, "history": history}


# ---------- 9. 应用信息（公开） ----------
@router.get("/info")
def get_app_info():
    from src.core.config import settings
    return {"app_name": settings.app_name, "version": settings.app_version, "debug": settings.debug}


# ---------- 10. 健康检查（公开） ----------
@router.get("/health")
def health_check():
    return {"status": "ok", "version": "v1"}


# ---------- 11. 发送验证码 ----------
@router.post("/send-verification")
async def send_verification(req: EmailRequest):
    email = req.email
    code = str(random.randint(100000, 999999))
    verification_codes[email] = {"code": code, "expire": time.time() + 600}
    await send_verification_email(email, "user", code)
    return {"message": "Verification code sent (check console)"}


# ---------- 12. 校验验证码 ----------
@router.post("/verify-email")
def verify_email(req: VerifyEmailRequest):
    email = req.email
    code = req.code
    record = verification_codes.get(email)
    if not record:
        raise HTTPException(status_code=400, detail="No verification code found for this email")
    if time.time() > record["expire"]:
        raise HTTPException(status_code=400, detail="Code expired")
    if record["code"] != code:
        raise HTTPException(status_code=400, detail="Invalid code")
    return {"message": "Email verified successfully"}


# ---------- 13. W3 预览（占位） ----------
@router.get("/preview/w3")
def w3_preview():
    return {"message": "W3 准备就绪，即将接入大模型！", "status": "ready"}


# ---------- 14. RAG 知识库问答 ----------
@router.post("/rag", response_model=RAGResponse)
@limiter.limit("5/minute")
async def rag_endpoint(
    request: Request,
    rag_req: RAGRequest,
    current_user: dict = Depends(get_current_user),
):
    """RAG 知识库问答，返回带引用的答案"""
    result = await rag_answer(
        query=rag_req.query,
        top_k=rag_req.top_k or 3,
        temperature=rag_req.temperature or 0.3,
    )
    return RAGResponse(
        answer=result["answer"],
        sources=result["sources"],
        has_answer=result["has_answer"],
    )

# ---------- 14. 简历解析 ----------
@router.post("/resume/parse")
async def parse_resume_endpoint(
    data: ResumeTextInput,
    current_user: dict = Depends(get_current_user),
):
    resume = await parse_resume(data.text)
    return resume.model_dump()

# ---------- 15. JD 分析 ----------
@router.post("/jd/analyze")
async def analyze_jd_endpoint(
    data: JDTextInput,
    current_user: dict = Depends(get_current_user),
):
    # 需要先解析简历，简化为传入完整 resume 对象
    # 应从数据库读取，先留占位
    return {"message": "需要传入 resume 对象"}

# ---------- 16. 定制化简历 ----------
@router.post("/cv/tailor")
async def tailor_cv_endpoint(
    data: TailorRequest,
    current_user: dict = Depends(get_current_user),
):
    resume = await parse_resume(data.resume_text)
    result = await tailor_cv(resume, data.jd_text)
    return result.model_dump()