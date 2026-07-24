from fastapi import FastAPI

app = FastAPI(
    title="AI Engineer Roadmap",
    version="0.1.0",
    description="W1 环境搭建完成，W2 正式启动 FastAPI 开发"
)

@app.get("/")
def root():
    return {"message": "✅ W1 Complete! Ready for FastAPI."}

@app.get("/health")
def health_check():
    return {"status": "ok"}