# Week 1 复盘（7/17 – 7/23）

## 🎯 本周核心目标
- [x] Python 3.11+ 环境（pyenv + uv）搭建完成
- [x] GitHub 作品集仓库初始化，每日 commit ≥1 次
- [x] 类型注解 + Pydantic v2 数据校验跑通
- [x] 自定义异常体系 + 细粒度 try/except
- [x] async/await 异步基础 + asyncio.gather 并发
- [x] 手写上下文管理器（with 语句）
- [x] 工程规范：Ruff + MyPy 配置完成
- [x] 日志系统（带轮转）落地
- [x] asyncio.Semaphore 并发限流 demo
- [x] LeetCode 数组/哈希表 **累计 10 题**

## 🛠 已安装工具链
| 工具 | 用途 |
|------|------|
| Python 3.11.8 | 核心解释器（pyenv 管理） |
| uv | 极速依赖管理（替代 pip/poetry） |
| Ruff | 代码格式化 + Linting（替代 black+flake8） |
| MyPy | 静态类型检查 |
| Pydantic v2 | 数据校验与序列化 |
| Git + GitHub | 版本控制与作品托管 |

## 📂 项目结构
ai-engineer-roadmap/
├── src/ # 核心业务代码
│ ├── models/ # Pydantic / SQLAlchemy 模型
│ ├── services/ # 业务逻辑
│ ├── utils/ # 日志、异常、工具函数
│ └── api/ # FastAPI 路由（W2 新增）
├── sandbox/ # W1 练习沙盒文件（归档）
├── leetcode/ # 算法题解
├── logs/ # 日志文件（自动生成）
├── pyproject.toml # 项目依赖 + 工具配置
└── README.md

## 🧠 核心技术收获
1. **类型注解 + MyPy**：早于运行时发现类型错误，适合大型项目协作。
2. **Pydantic v2**：`EmailStr`、`Field` 校验、`model_dump()` 序列化。
3. **异步并发**：`asyncio.gather` 总耗时取决于最慢任务，而非总和。
4. **上下文管理器**：用 `__enter__`/`__exit__` 或 `@contextmanager` 保证资源释放。
5. **日志轮转**：`RotatingFileHandler` 按大小切割，生产环境必备。
6. **Semaphore**：控制并发数，防止 API 被限流。

## Week 2 复盘（7/24 – 7/30）

### 🎯 本周核心目标
- [x] FastAPI 路由、路径参数、查询参数、请求体
- [x] 依赖注入（Depends）分层架构（Router → Service → Repository）
- [x] 配置管理（pydantic-settings + .env）
- [x] PostgreSQL 接入 + SQLModel + Alembic 迁移
- [x] JWT 认证（注册/登录/Token 校验）
- [x] 邮箱验证码发送与校验
- [x] 接口限流（slowapi，5次/分钟）
- [x] LeetCode 双指针/滑动窗口累计 10 题

### 🛠️ 本周新增工具链
| 工具 | 用途 |
|------|------|
| FastAPI + Uvicorn | Web 框架与 ASGI 服务器 |
| SQLModel + Alembic | ORM 与数据库迁移 |
| PostgreSQL | 生产级关系数据库 |
| python-jose | JWT 签发与验证 |
| passlib[bcrypt] | 密码哈希 |
| slowapi | 接口限流 |
| fastapi-mail | 邮件发送 |
| openai + langchain | W3 预装，AI 调用（下周启用） |

### 📂 项目结构更新
ai-engineer-roadmap/
├── .env                           # 环境变量（数据库 URL、JWT 密钥、邮件配置）
├── .gitignore                     # Git 忽略规则
├── pyproject.toml                 # 项目依赖（uv 管理）
├── uv.lock                        # 依赖锁文件
├── README.md                      # 项目文档（含 W1/W2 复盘）
├── alembic.ini                    # Alembic 迁移配置
│
├── alembic/                       # 数据库迁移管理
│   ├── env.py                     # 迁移环境配置（已接入 SQLModel）
│   ├── script.py.mako             # 迁移脚本模板
│   └── versions/                  # 所有迁移版本
│       ├── 033a382ca768_create_message_table.py
│       └── d55e43f9e6f0_add_user_table.py
│
├── sandbox/                       # W1 练习沙盒（已归档，保留备用）
│   ├── sandbox_async.py
│   ├── sandbox_basic.py
│   ├── sandbox_context.py
│   ├── sandbox_decorator.py
│   ├── sandbox_exception.py
│   ├── sandbox_generator.py
│   ├── sandbox_pydantic.py
│   ├── sandbox_semaphore.py
│   └── sandbox_type.py
│
├── logs/                          # 日志文件（自动生成）
│   └── app.log
│
└── src/                           # 核心源码（所有业务代码）
    ├── main.py                    # FastAPI 应用入口（含限流中间件）
    ├── __init__.py
    │
    ├── api/                       # 接口层（路由 + 依赖注入 + 限流）
    │   ├── dependencies.py        # 核心依赖：get_db、get_current_user、get_settings
    │   ├── rate_limit.py          # 限流器实例（slowapi）
    │   ├── v1/                    # API v1 版本
    │   │   ├── endpoints.py       # 所有路由（注册、登录、聊天、历史、验证码）
    │   │   └── __init__.py
    │   └── __pycache__/
    │
    ├── core/                      # 核心配置与安全
    │   ├── config.py              # pydantic-settings 配置加载
    │   ├── security.py            # JWT 签发/验证 + bcrypt 密码哈希
    │   └── __init__.py
    │
    ├── models/                    # 数据模型
    │   ├── db_models.py           # SQLModel 表定义（User, Message）
    │   ├── user.py                # Pydantic 请求/响应模型（已迁移到 endpoints 内联）
    │   └── __pycache__/
    │
    ├── repositories/              # 数据访问层（Repository 模式）
    │   ├── memory_db.py           # 内存存储（早期原型，保留参考）
    │   ├── message_repo.py        # 消息 CRUD（PostgreSQL 实现）
    │   ├── user_repo.py           # 用户 CRUD（PostgreSQL 实现）
    │   └── __init__.py
    │
    ├── services/                  # 业务逻辑层（Service 模式）
    │   ├── chat_service.py        # 对话业务逻辑（处理消息、调用 Repository）
    │   ├── llm_service.py         # W3 预占位（AI 调用）
    │   └── __pycache__/
    │
    ├── utils/                     # 工具函数
    │   ├── email.py               # 邮件发送（验证码）
    │   ├── exceptions.py          # 自定义异常
    │   ├── logger.py              # 日志配置（RotatingFileHandler）
    │   └── __pycache__/
    │
    └── __pycache__/

### 🧠 核心技术收获
1. **FastAPI 依赖注入**：用 `Depends()` 管理数据库 Session、配置、认证，实现控制反转。
2. **分层架构**：Router → Service → Repository，职责清晰，更换数据库时只需改 Repository。
3. **JWT 认证**：`/register` 和 `/login` 返回 Token，受保护接口必须携带 `Authorization: Bearer <token>`。
4. **限流保护**：`/chat` 限制 5 次/分钟，防止 API 滥用。
5. **Alembic 迁移**：代码改表结构后，`alembic revision --autogenerate` + `alembic upgrade head` 自动同步数据库。
6. **邮箱验证**：注册时发送 6 位验证码，有效期 10 分钟（内存存储，生产可用 Redis）。