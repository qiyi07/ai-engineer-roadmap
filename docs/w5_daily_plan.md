# W5 每日作战计划（8/14 起 — 进行中）

> 依据 GitHub 仓库（qiyi07/ai-engineer-roadmap）实际提交历史整理。
> 仅保留与文件创建/修改相关的实操内容；已删除算法题、面试准备、简历投递等非文件类任务。
> 提交哈希为 `git log` 实测值，文件清单来自每次提交的 `--name-only` 输出。

## 📅 每日明细

### Day 1 · 8/14（周五）— 项目4 启动：结构化输出 + Tool Calling
- **提交**：`00033d6`（W5-Day1: project4 start - structured output & tool calling, agent dem0）
- **涉及文件**：
  - `src/agents/__init__.py`
  - `src/agents/schemas.py` —— 结构化输出模型（Pydantic）
  - `src/agents/tools.py` —— 工具定义与注册
  - `src/agents/agent_service.py` —— Agent 服务（Tool Calling 循环）
  - `test/test_agent.py` —— Agent 测试
- **验收**：LLM 输出被校验为结构化数据；工具调用可触发

### Day 2 · 8/14（周五）— 多步任务 Agent + Agentic RAG
- **提交**：`04ec2e5`（W5-Day2: multi-step agent, agentic RAG）
- **涉及文件**：
  - `src/agents/agent_service.py` —— 多步任务编排（多轮工具调用）
  - `src/agents/tools.py` —— 新增 RAG 检索工具（Agentic RAG）
  - `test/test_agent.py` —— 多步/agentic 场景测试
- **验收**：Agent 可自主规划并连续调用多个工具完成多步任务

### Day 3 · 8/14（周五）— MCP Demo
- **提交**：`1d5048c`（W5-Day3: MCP demo）
- **涉及文件**：
  - `pyproject.toml` —— MCP 依赖
  - `src/agents/mcp_demo.py` —— MCP 演示脚本
  - `docs/resume_projects.md` —— 简历项目文档（新建）
- **验收**：MCP demo 可运行并演示工具接入

### Day 4 · 8/14（周五）— MCP 真实 Demo + Agent 状态流图
- **提交**：`b362c13`（W5-Day4: MCP real demo, agent state flow diagram）
- **涉及文件**：
  - `src/agents/mcp_server.py` —— MCP 服务端
  - `src/agents/mcp_client.py` —— MCP 客户端
  - `docs/agent_state_flow.png` —— Agent 状态流程图
- **验收**：MCP client↔server 真实联通；状态流图产出

### Day 5 · 8/15（周六）— 项目4 收尾
- **提交**：`67f05ff`（W5-Day5: project4 final wrap-up, job tracking updated, interview prep started）
- **涉及文件**：
  - `docs/agent_architecture.png` —— Agent 架构图
- **验收**：项目 4（AI Agent 工具助手）达成完整交付

## ✅ W5 当前进度（实测）

```
ai-engineer-roadmap/
├── src/agents/
│   ├── schemas.py           # 结构化输出模型
│   ├── tools.py             # 工具定义（含 RAG 工具）
│   ├── agent_service.py     # 多步 Agent 编排
│   ├── mcp_demo.py          # MCP 演示
│   ├── mcp_server.py        # MCP 服务端
│   └── mcp_client.py        # MCP 客户端
├── docs/
│   ├── agent_architecture.png  # Agent 架构图
│   ├── agent_state_flow.png    # 状态流程图
│   └── resume_projects.md      # 简历项目文档
└── test/test_agent.py          # Agent 测试
```

> 注：W5 计划按 8/14 起实际提交时间记录，单日多提交（Day1–4 均在 8/14 完成），后续任务继续进行。
