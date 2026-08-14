from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from src.services.llm_service import llm  # 你已有的 LLM 实例
from src.agents.tools import get_weather, calculate, search_web
from src.agents.tools import weather_tool, calculate_tool, search_tool, rag_search_tool

@tool
def weather_tool(city: str) -> str:
    """查询城市的天气信息"""
    data = get_weather(city)
    return f"{data['city']} 天气：{data['condition']}，温度 {data['temperature']}°C"


@tool
def calculate_tool(expression: str) -> str:
    """执行数学计算，输入表达式如 '2+3*4'"""
    try:
        result = calculate(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {e}"


@tool
def search_tool(query: str) -> str:
    """搜索网页信息"""
    results = search_web(query)
    return "\n".join(results[:3])


# ---------- 工具列表 ----------
tools = [weather_tool, calculate_tool, search_tool, rag_search_tool]


# ---------- 创建 Agent ----------
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个有用的智能助手，可以使用工具帮助用户。"),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"),
# ])
# src/agents/agent_service.py（更新 prompt）
# prompt = ChatPromptTemplate.from_messages([
#     ("system", """你是一个智能助手，可以使用工具解决复杂问题。
# 你可以分步执行：先调用一个工具获取信息，然后根据结果决定下一步。
# 例如：用户问“北京天气适合穿什么？”，你应该先调用天气工具，再根据温度给出建议。"""),
#     ("human", "{input}"),
#     ("placeholder", "{agent_scratchpad}"),
# ])
prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个智能助手，可以使用工具帮助用户。
可用工具：
- 天气工具（weather_tool）：查询城市天气，输入城市名。
- 计算器工具（calculate_tool）：执行数学计算，如 "2+3*4"。
- 搜索工具（search_tool）：搜索网络信息，输入关键词。
- 知识库工具（rag_search_tool）：查询内部知识库，适用于专业问题（如机器学习、编程等）。

请根据用户问题选择合适的工具，必要时可组合使用多个工具。"""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# ---------- 对外接口 ----------
def chat_with_agent(user_input: str) -> str:
    """与 Agent 对话，自动调用工具"""
    result = agent_executor.invoke({"input": user_input})
    return result["output"]