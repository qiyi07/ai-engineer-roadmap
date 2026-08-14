import requests
import math
from src.services.rag_service import rag_answer
def get_weather(city: str) -> dict:
    """获取天气（模拟）"""
    # 实际可调用 API，这里模拟
    return {"city": city, "temperature": 22, "condition": "晴", "humidity": 60}

def calculate(expression: str) -> float:
    """执行简单数学计算（安全限制）"""
    # 仅允许数字和基本运算符
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expression):
        raise ValueError("包含非法字符")
    return eval(expression)

def search_web(query: str) -> list:
    """模拟网页搜索"""
    # 返回固定的示例结果
    return [f"关于 '{query}' 的结果1", f"关于 '{query}' 的结果2"]

# src/agents/tools.py（追加）


@tool
def rag_search_tool(query: str) -> str:
    """从知识库中检索相关文档并回答问题。当用户询问专业领域知识时使用此工具。"""
    result = asyncio.run(rag_answer(query))
    if result["has_answer"]:
        return result["answer"]
    else:
        return "知识库中没有找到相关信息。"