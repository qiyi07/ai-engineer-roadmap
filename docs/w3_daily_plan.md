# W3 每日作战计划（7/31 – 8/6）

> 依据 GitHub 仓库（qiyi07/ai-engineer-roadmap）实际提交历史整理。
> 仅保留与文件创建/修改相关的实操内容；已删除算法题、面试准备、简历投递等非文件类任务。
> 提交哈希为 `git log` 实测值，文件清单来自每次提交的 `--name-only` 输出。

## 📅 每日明细

### Day 1 · 7/31（周五）— 接入真实 LLM + 流式接口
- **提交**：`6d2c7e6`（W3-Day1: streaming endpoint, chat with real LLM）
- **涉及文件**：
  - `pyproject.toml` —— openai / langchain 依赖生效
  - `src/core/config.py` —— DEEPSEEK_API_KEY 等模型配置
  - `src/services/llm_service.py` —— LLM 调用封装（OpenAI 兼容接口）
  - `src/services/chat_service.py` —— 对话业务接入 LLM
  - `src/api/v1/endpoints.py` —— `/chat` 流式接口
  - `src/api/rate_limit.py`、`src/main.py` —— 限流与路由挂载
  - `test_llm.py` —— LLM 调用测试
- **验收**：`/chat` 返回真实模型回复；`test_llm.py` 通过
- **附带**：`a733c0d`（chore: add .env.example template）—— 新增 `.env.example` 模板

### Day 2 · 8/1（周六）— Prompt 模板 + LCEL + 多轮上下文
- **提交**：`14c4608`（W3-Day2: prompt templates, LCEL, multi-turn conversation context）
- **涉及文件**：
  - `.env.example` —— 更新模板
  - `src/core/config.py`、`src/main.py`
  - `src/services/chat_service.py` —— 多轮上下文拼接
  - `src/services/llm_service.py` —— PromptTemplate / ChatPromptTemplate / LCEL 链
- **验收**：多轮对话携带历史上下文；LCEL 链式调用可复用

### Day 3 · 8/2（周日）— 流式前端 + 项目1 完成
- **提交**：`00aca4e`（W3-Day3: streaming frontend, project1 complete - AI chat assistant）
- **涉及文件**：
  - `static/index.html` —— 聊天页面（打字机效果）
  - `src/main.py` —— 静态文件服务挂载
- **验收**：浏览器可对话，流式打字机效果正常；AI 聊天助手项目 1 完成

### Day 4 · 8/3（周一）— Supabase 云数据库 + 部署就绪
- **提交**：`519aa67`（ready for railway deployment with supabase）
- **涉及文件**：
  - `Dockerfile` —— 容器化配置
  - `requirements.txt` —— 部署依赖清单
  - `alembic.ini`、`alembic/env.py` —— 迁移环境适配云库
  - `alembic/versions/033a382ca768_create_message_table.py`、`alembic/versions/ca184acdaf56_init_tables.py`
  - `src/core/config.py` —— 切换 Supabase（含 SSL）连接串
- **验收**：本地连接 Supabase 成功；镜像构建通过

### Day 5 · 8/4（周二）— 多会话支持
- **提交**：`5103f54`（W3-Day5: multi-session support, session CRUD, message isolation）
- **涉及文件**：
  - `alembic/versions/3277eda376fd_add_chat_session_table.py` —— ChatSession 表迁移
  - `src/models/db_models.py` —— ChatSession 表定义
  - `src/repositories/session_repo.py` —— 会话 CRUD
  - `src/repositories/message_repo.py`、`src/services/chat_service.py`、`src/api/v1/endpoints.py` —— 会话上下文隔离
- **验收**：可创建/切换/删除会话；各会话消息互不干扰

### Day 6 · 8/5（周三）— 自动标题 + 前端会话支持
- **提交**：`5673af0`（W3-Day6: auto session title generation, frontend session support, code cleanup）
- **涉及文件**：
  - `src/services/llm_service.py` —— 基于首条消息自动生成标题
  - `src/services/chat_service.py`、`src/api/v1/endpoints.py` —— 标题生成接入
  - `static/index.html`、`static/app.js`、`static/style.css` —— 前端会话列表/切换
- **验收**：新会话自动命名；前端可切换会话查看历史

### Day 7 · 8/6（周四，收尾）— RAG 预装 + 周复盘
- **提交**：`bf18169`（W3-Final: project2 complete, README updated）
- **涉及文件**：
  - `README.md` —— W3 复盘
  - `pyproject.toml` —— 预装 W4 RAG 依赖（sentence-transformers、pgvector 等）
  - `src/rag/__init__.py`、`src/rag/document_loader.py`、`src/rag/vector_store.py` —— RAG 模块骨架预建
- **验收**：README 更新；RAG 模块目录就绪

## ✅ W3 结束时的项目结构（实测）

```
ai-engineer-roadmap/
├── Dockerfile / requirements.txt    # 容器化部署
├── static/                          # 前端（index.html + app.js + style.css）
├── src/
│   ├── main.py                      # 入口（含静态服务）
│   ├── api/v1/endpoints.py          # 聊天 + 会话路由
│   ├── services/
│   │   ├── chat_service.py          # 多会话业务
│   │   └── llm_service.py           # LCEL 链 + 标题生成
│   ├── repositories/session_repo.py # 会话 CRUD
│   ├── rag/                         # W4 预建（document_loader / vector_store）
│   └── models/db_models.py          # + ChatSession 表
└── README.md                        # W1-W3 复盘
```
