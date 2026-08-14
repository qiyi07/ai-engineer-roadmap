import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.agents.agent_service import extract_weather_info, chat_with_agent


def test_extract_weather():
    """测试结构化提取天气信息"""
    print("=" * 50)
    print("测试：结构化提取天气信息")
    print("=" * 50)
    result = extract_weather_info("今天北京25度，晴，微风")
    print(f"城市: {result.city}")
    print(f"温度: {result.temperature}°C")
    print(f"天气: {result.condition}")
    print(f"湿度: {result.humidity}")
    print(f"风速: {result.wind_speed}")


def test_multi_step():
    """测试 Agent 多步推理"""
    print("\n" + "=" * 50)
    print("测试：Agent 多步推理（天气 + 推荐）")
    print("=" * 50)
    query = "北京今天天气怎么样？如果温度高于20度，推荐一个户外活动。"
    response = chat_with_agent(query)
    print(f"Agent 回答: {response}")


def test_agent_calculation():
    """测试 Agent 计算能力"""
    print("\n" + "=" * 50)
    print("测试：Agent 计算")
    print("=" * 50)
    query = "计算 25 * 4 + 10 等于多少？"
    response = chat_with_agent(query)
    print(f"Agent 回答: {response}")


def test_agent_rag():
    """测试 Agent 调用 RAG 工具"""
    print("\n" + "=" * 50)
    print("测试：Agentic RAG")
    print("=" * 50)
    query = "什么是监督学习？"
    response = chat_with_agent(query)
    print(f"Agent 回答: {response}")


if __name__ == "__main__":
    # 运行所有测试
    test_extract_weather()
    test_multi_step()
    test_agent_calculation()
    test_agent_rag()