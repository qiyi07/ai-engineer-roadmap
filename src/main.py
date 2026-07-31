from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from src.api.v1.endpoints import router
from src.api.rate_limit import limiter

app = FastAPI(
    title="AI Engineer Roadmap",
    version="0.2.0",
    description="W2: FastAPI 路由与参数实战 + 限流"
)

# ---------- 限流配置 ----------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ---------- 挂载路由 ----------
app.include_router(router)

# ---------- 根路径 ----------
@app.get("/")
def root():
    return {"message": "✅ W2 Started! Visit /docs for Swagger UI (Rate limiting enabled)"}