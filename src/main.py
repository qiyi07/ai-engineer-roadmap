# from fastapi import FastAPI
# from slowapi.middleware import SlowAPIMiddleware
# from slowapi.errors import RateLimitExceeded
# from slowapi import _rate_limit_exceeded_handler
# from src.api.v1.endpoints import router
# from src.api.rate_limit import limiter

# app = FastAPI(
#     title="AI Engineer Roadmap",
#     version="0.2.0",
#     description="W2: FastAPI 路由与参数实战 + 限流"
# )

# # ---------- 限流配置 ----------
# app.state.limiter = limiter
# app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# app.add_middleware(SlowAPIMiddleware)

# # ---------- 挂载路由 ----------
# app.include_router(router)

# # ---------- 根路径 ----------
# @app.get("/")
# def root():
#     return {"message": "W2 Started! Visit /docs for Swagger UI (Rate limiting enabled)"}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from src.api.v1.endpoints import router
from src.api.rate_limit import limiter
from fastapi.openapi.utils import get_openapi

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

# ---------- 挂载静态文件（前端聊天页面） ----------
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# ---------- 自定义 OpenAPI（为 Swagger 添加 Bearer 认证按钮） ----------
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi