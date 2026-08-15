# W4 每日作战计划（8/7 – 8/13）

> 依据 GitHub 仓库（qiyi07/ai-engineer-roadmap）实际提交历史整理。
> 仅保留与文件创建/修改相关的实操内容；已删除算法题、面试准备、简历投递等非文件类任务。
> 提交哈希为 `git log` 实测值，文件清单来自每次提交的 `--name-only` 输出。

## 📅 每日明细

### Day 1 · 8/7（周五）— pgvector + Embedding 存储/检索
- **提交**：`fe18b55`（W4-Day1: pgvector setup, embedding storage & retrieval, test_vector.py）
- **涉及文件**：
  - `src/rag/vector_store.py` —— PGVector 向量存储与检索
  - `test_vector.py` —— 向量读写测试（根目录版）
- **验收**：向量可写入并检索；相似度排序正确

### Day 2 · 8/8（周六）— 文档加载 + 文本切分 + 链路测试
- **提交**：`bea984e`（W4-Day2: document loader, text splitter, metadata, full RAG pipeline test）
- **涉及文件**：
  - `pyproject.toml` —— RAG 依赖（pypdf、rank-bm25、jieba 等）
  - `src/rag/document_loader.py` —— 多格式加载（TXT/Markdown/PDF）
  - `src/rag/text_splitter.py` —— chunk_size/overlap 切分
  - `src/rag/vector_store.py` —— 元数据管理（页码/来源）
  - `src/core/config.py` —— 向量库连接配置
  - `test/test_rag_pipeline.py`、`test/test_vector.py`、`test/test_llm.py` —— 链路测试
  - `test/sample.txt`、`sandbox/check_db.py`、`static/index.html`、`static/app.js`
  - `test_vector.py` —— 迁移到 test/ 目录
- **验收**：TXT/MD/PDF 均可加载入库；切分与检索测试通过

### Day 3 · 8/9（周日）— 完整 RAG 链路（检索+生成+兜底+引用）
- **提交**：`86fd161`（W4-Day3: full RAG pipeline (retrieval + generation + fallback + sources)）
- **涉及文件**：
  - `src/services/rag_service.py` —— RAG 问答服务（检索→拼接→LLM→返回）
  - `src/rag/vector_store.py` —— 相似度阈值过滤
  - `src/api/v1/endpoints.py` —— RAG 问答接口
  - `test/test_rag.py` —— RAG 链路测试
- **验收**：回答带引用来源；检索不到时明确提示（不胡编）

### Day 4 · 8/10（周一）— 混合检索 + 调优实验
- **提交**：`5280f60`（W4-Day4: retrieval tuning, hybrid BM25+vector, evaluation experiments）
- **涉及文件**：
  - `pyproject.toml` —— rank-bm25、jieba 依赖
  - `src/rag/hybrid_retriever.py` —— BM25 + 向量混合检索
  - `src/rag/evaluator.py` —— 检索质量评估
  - `src/rag/vector_store.py` —— topK / threshold 参数化
  - `src/services/rag_service.py` —— 接入混合检索
  - `experiments/chunk_experiment.py` —— chunk 大小调优实验
  - `data/eval_queries.json` —— 评测数据集
  - `sample.txt` —— 实验语料
- **验收**：混合检索召回率提升；调优实验有对比数据

### Day 5 · 8/11（周二，收尾）— 项目3 验收 + 周复盘
- **提交**：`6f8006a`（W4-Final: project3 complete, RAG pipeline, evaluation, README updated）
- **涉及文件**：
  - `README.md` —— W4 复盘（含调优结论）
  - `src/rag/vector_store.py`、`src/rag/text_splitter.py` —— 定稿
  - `test/test_rag.py`、`test/test_document_loader.py` —— 回归测试
  - `sample.md`、`sample.pdf` —— 样例文档
  - `sandbox/sandbox_basic.py`、`sandbox/sandbox_exception.py` —— 沙盒清理
- **验收**：项目 3 量化验收达成（≥2格式、带引用、有兜底、有调优数据）

### Day 6 · 8/12（周三）— RAG SSL 修复 + 项目5 原型（简历优化）
- **提交**：`055578c`（W4-Day6: RAG SSL fix, project5 resume optimizer prototype）
- **涉及文件**：
  - `src/projects/__init__.py`、`src/projects/resume_optimizer/__init__.py`
  - `src/projects/resume_optimizer/prompts.py` —— 简历优化 Prompt 模板
  - `src/projects/resume_optimizer/schemas.py` —— 结构化输出模型
  - `src/projects/resume_optimizer/service.py` —— 优化服务
  - `test/test_resume.py` —— 简历优化测试
- **验收**：RAG SSL 连接问题修复；简历优化原型可跑

### Day 7 · 8/13（周四，收尾）— 项目5 完成 + 全量回归
- **提交**：`4faf5b5`（W4-Final: project5 complete, RAG pipeline stable, README updated）
- **涉及文件**：
  - `src/projects/resume_optimizer/prompts.py` / `schemas.py` / `service.py` —— 定稿
  - `src/api/v1/endpoints.py` —— 简历优化接口
  - `test/test_resume.py` —— 测试补全
- **验收**：项目 5 完成；RAG 管线稳定；全量测试通过

## ✅ W4 结束时的项目结构（实测）

```
ai-engineer-roadmap/
├── data/eval_queries.json          # 评测数据集
├── experiments/chunk_experiment.py # 调优实验
├── sample.md / sample.pdf / sample.txt
├── src/
│   ├── rag/
│   │   ├── document_loader.py      # 多格式加载
│   │   ├── text_splitter.py        # 文本切分
│   │   ├── vector_store.py         # PGVector 存储/检索
│   │   ├── hybrid_retriever.py     # BM25+向量混合
│   │   └── evaluator.py            # 检索评估
│   ├── services/rag_service.py     # RAG 问答服务
│   ├── projects/resume_optimizer/  # 项目5：简历优化
│   └── api/v1/endpoints.py         # + RAG/简历接口
├── test/                           # test_rag / vector / pipeline / resume ...
└── README.md                       # W1-W4 复盘
```
