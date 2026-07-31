import asyncio
from src.services.llm_service import chat_with_llm_stream

async def test():
    print("开始测试 DeepSeek 流式对话...\n")
    async for chunk in chat_with_llm_stream("你好，请用一句话简单介绍自己"):
        print(chunk, end="")
    print("\n\n测试完成！")

if __name__ == "__main__":
    asyncio.run(test())