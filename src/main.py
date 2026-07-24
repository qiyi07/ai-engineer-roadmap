from fastapi import FastAPI
from src.api.v1.endpoints import router

app = FastAPI(
    title="AI Engineer Roadmap",
    version="0.2.0",
    description="W2: FastAPI 路由与参数实战"
)

# 挂载 v1 路由
app.include_router(router)

# 根路径（兼容旧访问）
@app.get("/")
def root():
    return {"message": "✅ W2 Started! Visit /docs for Swagger UI"}