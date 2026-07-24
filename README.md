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