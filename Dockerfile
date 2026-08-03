# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装 uv（包管理器）
RUN pip install uv

# 复制依赖文件
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 复制源码
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]