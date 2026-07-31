from typing import AsyncGenerator, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.core.config import settings

# 初始化 DeepSeek（兼容 OpenAI）
llm = ChatOpenAI(
    model=settings.openai_model,
    temperature=0.7,
    openai_api_key=settings.openai_api_key,
    openai_api_base=settings.openai_base_url,
)

async def chat_with_llm_stream(
    user_message: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    """流式调用 LLM，yield 增量内容"""
    if system_prompt is None:
        system_prompt = "You are a helpful AI assistant."

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]

    async for chunk in llm.astream(messages):
        content = chunk.content
        if content:
            yield content


async def chat_with_llm_complete(
    user_message: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    """非流式调用，返回完整回复"""
    if system_prompt is None:
        system_prompt = "You are a helpful AI assistant."

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message),
    ]

    response = await llm.ainvoke(messages)
    return response.content