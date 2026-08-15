# W1 每日作战计划（7/17 – 7/24）

> 依据 GitHub 仓库（qiyi07/ai-engineer-roadmap）实际提交历史整理。
> 仅保留与文件创建/修改相关的实操内容；已删除算法题、面试准备、简历投递等非文件类任务。
> 提交哈希为 `git log` 实测值，文件清单来自每次提交的 `--name-only` 输出。

## 📅 每日明细

### Day 1 · 7/17（周五）— 项目初始化
- **提交**：`6e55212` / `696511e`（init: project skeleton with uv）
- **涉及文件**：
  - `.gitignore` —— Python 模板（忽略 .venv、__pycache__、logs 等）
- **内容要点**：uv 初始化项目骨架；Git 仓库建立；首次 commit
- **验收**：GitHub 仓库可见首次提交；`git log` 有记录

### Day 2 · 7/18（周六）— 类型注解 + Pydantic + 基础语法
- **提交**：`d1841ee`（W1-Day2: type hints, pydantic v2 validation, basic syntax drills）
- **涉及文件**：
  - `sandbox_type.py` —— 带类型注解的函数（`list[str]`、`Optional`）
  - `sandbox_pydantic.py` —— Pydantic v2 模型（`EmailStr`、`Field`、`model_dump()`）
  - `sandbox_basic.py` —— 列表/字典推导式、细粒度 try/except、with open
  - `pyproject.toml` / `uv.lock` —— 添加 pydantic、email-validator、mypy 依赖
- **验收**：`mypy sandbox_type.py` 零报错；pydantic 校验拦截正常输出

### Day 3 · 7/19（周日）— 装饰器 + 生成器
- **提交**：`e4aa0f6`（W1-Day3: decorator, generator）
- **涉及文件**：
  - `sandbox_decorator.py` —— 手写 `@log_time` 装饰器统计函数耗时
  - `sandbox_generator.py` —— 生成器逐行读取大文件（`yield`）
- **验收**：装饰器能在控制台打印耗时；生成器可 `for line in ...` 逐行迭代

### Day 4 · 7/20（周一）— 自定义异常 + 异步
- **提交**：`8cf285a`（W1-Day4: custom exceptions, async/await gather）
- **涉及文件**：
  - `sandbox_exception.py` —— 自定义异常类（`class APIError(Exception)`）
  - `sandbox_async.py` —— `asyncio.gather` 并发执行
- **验收**：异常按类型区分捕获；并发任务全部完成且总耗时≈最慢任务

### Day 5 · 7/21（周二）— 上下文管理器 + 项目结构
- **提交**：`2968707`（W1-Day5: context manager, project structure）
- **涉及文件**：
  - `sandbox_context.py` —— 手写上下文管理器（`__enter__`/`__exit__`）
  - `src/models/user.py` —— User Pydantic 模型
  - `src/utils/exceptions.py` —— 自定义异常体系（业务层）
  - `src/utils/logger.py` —— 日志配置
- **验收**：with 语句保证资源释放；异常/日志模块可被业务代码复用

### Day 6 · 7/22（周三）— 工程规范 + 并发限流
- **提交**：`3726c06`（W1-Day6: ruff/mypy config, logging with rotation, semaphore concurrency）
- **涉及文件**：
  - `pyproject.toml` —— Ruff + MyPy 工具配置
  - `sandbox_semaphore.py` —— `asyncio.Semaphore` 并发限流 demo
  - `src/utils/logger.py` —— `RotatingFileHandler` 日志轮转
  - `src/utils/exceptions.py` —— 异常体系完善
  - `logs/app.log` —— 日志文件（自动生成）
- **验收**：`ruff check` / `mypy` 通过；日志按大小轮转；Semaphore 控制并发数

### Day 7 · 7/24（周五，收尾）— 全量归档 + 工程骨架
- **提交**：`4cf4a08`（chore: correct .gitignore, include uv.lock）
  - `.gitignore` 修正；`uv.lock` 纳入版本控制
- **提交**：`bcee5ea`（W1-Final: full codebase with sandbox exercises, src structure, FastAPI skeleton）
  - **涉及文件**：
    - `sandbox/` —— 9 个沙盒文件归档到子目录（type/pydantic/basic/decorator/generator/exception/async/context/semaphore）
    - `src/__init__.py`、`src/main.py` —— FastAPI 应用入口骨架
    - `src/utils/logger.py` —— 日志模块定稿
    - `main.py` —— 根入口（过渡用）
    - `README.md` —— W1 复盘记录
    - `pyproject.toml` / `uv.lock` / `logs/app.log`
- **验收**：项目结构完整（sandbox 归档 + src 分层 + FastAPI 骨架）；README 记录 W1 复盘

## ✅ W1 结束时的项目结构（实测）

```
ai-engineer-roadmap/
├── .gitignore
├── pyproject.toml          # 依赖 + Ruff/MyPy 配置
├── uv.lock
├── README.md               # W1 复盘
├── main.py
├── logs/app.log            # 轮转日志
├── sandbox/                # 9 个沙盒练习文件（已归档）
└── src/
    ├── main.py             # FastAPI 入口
    ├── models/user.py      # Pydantic 模型
    └── utils/
        ├── exceptions.py   # 自定义异常
        └── logger.py       # 日志配置
```
