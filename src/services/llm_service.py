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
async def generate_session_title(user_message: str) -> str:
    """根据用户的第一条消息，生成简短的会话标题（≤20字）"""
    prompt = f"""请根据以下用户的第一条消息，生成一个简短的会话标题（不超过20个字）：
    
用户消息：{user_message}

标题："""
    
    # 使用非流式调用
    title = await chat_with_llm_complete(
        user_message=prompt,
        system_prompt="你是一个标题生成助手，只输出标题，不要有其他内容。",
        temperature=0.3,
    )
    # 清理换行和多余空格，限制长度
    title = title.strip()[:30]
    if not title or len(title) < 2:
        title = "新对话"
    return title