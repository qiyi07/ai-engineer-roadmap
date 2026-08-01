from typing import AsyncGenerator, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from src.core.config import settings

llm = ChatOpenAI(
    model=settings.openai_model,
    temperature=0.7,
    openai_api_key=settings.openai_api_key,
    openai_api_base=settings.openai_base_url,
)

def _build_chain(system_prompt: Optional[str] = None):
    """构建 LCEL 链，可定制 system prompt"""
    sys_msg = system_prompt or settings.system_prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    return prompt | llm | StrOutputParser()


async def chat_with_llm_stream(
    user_message: str,
    history: Optional[List[BaseMessage]] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
) -> AsyncGenerator[str, None]:
    """流式对话，支持历史消息"""
    # 温度需要动态设置，临时克隆 llm 并修改
    llm_with_temp = ChatOpenAI(
        model=settings.openai_model,
        temperature=temperature,
        openai_api_key=settings.openai_api_key,
        openai_api_base=settings.openai_base_url,
    )
    chain = _build_chain(system_prompt) | (lambda x: x)
    sys_msg = system_prompt or settings.system_prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    chain = prompt | llm_with_temp | StrOutputParser()
    
    async for chunk in chain.astream({
        "input": user_message,
        "history": history or [],
    }):
        yield chunk


async def chat_with_llm_complete(
    user_message: str,
    history: Optional[List[BaseMessage]] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    """非流式调用，返回完整回复"""
    llm_with_temp = ChatOpenAI(
        model=settings.openai_model,
        temperature=temperature,
        openai_api_key=settings.openai_api_key,
        openai_api_base=settings.openai_base_url,
    )
    sys_msg = system_prompt or settings.system_prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys_msg),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    chain = prompt | llm_with_temp | StrOutputParser()
    return await chain.ainvoke({
        "input": user_message,
        "history": history or [],
    })