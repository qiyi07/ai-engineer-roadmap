from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

from src.services.llm_service import llm  # 你已有的 LLM 实例
from src.agents.tools import get_weather, calculate, search_web
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
tools = [weather_tool, calculate_tool, search_tool]


# ---------- 创建 Agent ----------
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的智能助手，可以使用工具帮助用户。"),
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