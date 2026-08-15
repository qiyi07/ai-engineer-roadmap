# W2 每日作战计划（7/24 – 7/30）

> 依据 GitHub 仓库（qiyi07/ai-engineer-roadmap）实际提交历史整理。
> 仅保留与文件创建/修改相关的实操内容；已删除算法题、面试准备、简历投递等非文件类任务。
> 提交哈希为 `git log` 实测值，文件清单来自每次提交的 `--name-only` 输出。

## 📅 每日明细

### Day 1 · 7/24（周五）— FastAPI 路由入门
- **提交**：`e4971b3`（W2-Day1: FastAPI router with path/query/body params, swagger docs）
- **涉及文件**：
  - `src/main.py` —— 应用入口，挂载 v1 路由
  - `src/api/v1/__init__.py`
  - `src/api/v1/endpoints.py` —— 路径参数 / 查询参数 / 请求体 示例路由
- **验收**：`/docs` Swagger 自动文档可见；三类参数路由可调用

### Day 2 · 7/25（周六）— 依赖注入 + Service/Repo 分层
- **提交**：`1d3a2e8`（W2-Day2: DI, Service/Repo pattern, pydantic-settings）
- **涉及文件**：
  - `pyproject.toml` —— 添加 fastapi、pydantic-settings 等依赖
  - `src/core/__init__.py`、`src/core/config.py` —— pydantic-settings 配置加载
  - `src/api/dependencies.py` —— `get_settings` / `get_db` 依赖
  - `src/api/v1/endpoints.py` —— 路由注入依赖
  - `src/repositories/__init__.py`、`src/repositories/memory_db.py` —— 内存仓库
  - `src/services/chat_service.py` —— 业务逻辑层
- **验收**：Router → Service → Repository 三层调用链跑通

### Day 3 · 7/26（周日）— SQLModel + Alembic 迁移
- **提交**：`03755c3`（W2-Day3: SQLModel + Alembic migration, SQLite persistence）
- **涉及文件**：
  - `alembic.ini`、`alembic/README`、`alembic/env.py`、`alembic/script.py.mako` —— Alembic 迁移环境
  - `alembic/versions/033a382ca768_create_message_table.py` —— Message 表迁移
  - `src/models/db_models.py` —— SQLModel 表定义（Message）
  - `src/repositories/message_repo.py` —— 消息 CRUD（SQLite 实现）
  - `src/services/chat_service.py` —— 适配持久化存储
- **验收**：`alembic upgrade head` 建表成功；消息可持久化

### Day 4 · 7/27（周一）— PostgreSQL 接入 + Session 管理
- **提交**：`9be3808`（W2-Day4: PostgreSQL integration, DI Session management）
- **涉及文件**：
  - `pyproject.toml` —— 添加 psycopg/asyncpg 驱动
  - `alembic.ini` —— 数据库 URL 切到 PostgreSQL
  - `src/core/config.py` —— DATABASE_URL 配置
  - `src/api/dependencies.py` —— `get_db` 会话注入
  - `src/api/v1/endpoints.py`、`src/repositories/message_repo.py`、`src/services/chat_service.py` —— 适配 PG
- **验收**：PostgreSQL 建表成功；接口读写走 PG

### Day 5 · 7/28（周二）— JWT 认证
- **提交**：`981a007`（W2-Day5: JWT auth, user register/login, token validation）
- **涉及文件**：
  - `pyproject.toml` —— 添加 python-jose、passlib[bcrypt]
  - `alembic/versions/d55e43f9e6f0_add_user_table.py` —— User 表迁移
  - `src/core/security.py` —— JWT 签发/验证 + bcrypt 密码哈希
  - `src/core/config.py` —— JWT 密钥/过期配置
  - `src/models/db_models.py` —— User 表定义
  - `src/repositories/user_repo.py` —— 用户 CRUD
  - `src/api/dependencies.py` —— `get_current_user` 依赖
  - `src/api/v1/endpoints.py` —— 注册 / 登录 / 受保护接口
- **验收**：注册→登录→携带 Token 访问受保护接口全链路通

### Day 6 · 7/29（周三）— 邮箱验证 + 限流
- **提交**：`b7396e6`（W2-Day6: email verification, rate limiting）
- **涉及文件**：
  - `pyproject.toml` —— 添加 fastapi-mail、slowapi
  - `src/utils/email.py` —— 验证码邮件发送
  - `src/api/rate_limit.py` —— slowapi 限流器实例
  - `src/api/dependencies.py`、`src/api/v1/endpoints.py`、`src/main.py` —— 接入验证码校验与限流中间件
- **验收**：注册收到 6 位验证码；`/chat` 超频返回 429

### Day 7 · 7/30（周四，收尾）— 周复盘 + W3 预装
- **提交**：`a5546a2`（W2-Final: complete review, README update, W3 dependencies pre-installed）
- **涉及文件**：
  - `README.md` —— W2 复盘
  - `pyproject.toml` —— 预装 openai、langchain（W3 用）
  - 全量代码审查收尾：`src/main.py`、`src/api/*`、`src/core/*`、`src/models/*`、`src/repositories/*`、`src/services/*`、`src/utils/email.py`
- **验收**：W2 全部功能回归通过；README 更新

## ✅ W2 结束时的项目结构（实测）

```
ai-engineer-roadmap/
├── .env / .env.example          # 配置环境变量
├── alembic/                     # 数据库迁移（versions: message、user 表）
├── src/
│   ├── main.py                  # FastAPI 入口（含限流）
│   ├── api/
│   │   ├── dependencies.py      # get_db / get_current_user / get_settings
│   │   ├── rate_limit.py        # slowapi 实例
│   │   └── v1/endpoints.py      # 注册、登录、聊天、历史、验证码
│   ├── core/
│   │   ├── config.py            # pydantic-settings
│   │   └── security.py          # JWT + bcrypt
│   ├── models/db_models.py      # User、Message 表
│   ├── repositories/            # user_repo / message_repo / memory_db
│   ├── services/                # chat_service / llm_service（占位）
│   └── utils/email.py           # 验证码邮件
└── README.md                    # W1 + W2 复盘
```
