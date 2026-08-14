import requests
import math

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