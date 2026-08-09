from typing import List, Dict, Any, Optional
from src.rag.vector_store import search_with_threshold
from src.services.llm_service import chat_with_llm_complete
from src.core.config import settings

def format_context(chunks: List[dict]) -> str:
    """将检索到的文档块格式化为上下文文本"""
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk["metadata"].get("source", "未知来源")
        page = chunk["metadata"].get("page", "")
        page_info = f"（第{page}页）" if page else ""
        context_parts.append(
            f"【文档{i}】来自 {source}{page_info}\n{chunk['content']}\n"
        )
    return "\n".join(context_parts)


def build_prompt(query: str, context: str) -> str:
    """构建 RAG 提示词"""
    system_prompt = settings.system_prompt or (
        "你是一个专业的知识助手。请基于以下提供的文档内容回答用户问题。"
        "如果文档中没有相关信息，请明确告知用户你不知道，不要编造答案。"
    )
    return f"""{system_prompt}

【参考文档】
{context}

【用户问题】
{query}

请基于上述文档内容回答，并请在回答末尾用 `来源：` 列出你参考的文档编号（如“文档1、文档3”）。
如果文档中没有相关信息，请回复：“抱歉，我没有找到相关答案。”
"""


async def rag_answer(
    query: str,
    top_k: int = 3,
    score_threshold: float = 0.5,
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """
    RAG 问答完整链路
    返回: {
        "answer": str,
        "sources": List[dict],
        "has_answer": bool,
        "query": str,
    }
    """
    # 1. 检索相关文档块
    chunks = search_with_threshold(query, top_k=top_k, score_threshold=score_threshold)

    # 2. 如果无有效检索结果
    if not chunks:
        return {
            "answer": "抱歉，我没有找到相关答案。",
            "sources": [],
            "has_answer": False,
            "query": query,
        }

    # 3. 构建上下文和提示词
    context = format_context(chunks)
    prompt = build_prompt(query, context)

    # 4. 调用 LLM 生成答案
    reply = await chat_with_llm_complete(
        user_message=prompt,
        system_prompt="你是一个严谨的知识助手。",  # 这里会覆盖构建时的 system
        temperature=temperature,
    )

    # 5. 返回结果
    return {
        "answer": reply,
        "sources": chunks,
        "has_answer": True,
        "query": query,
    }