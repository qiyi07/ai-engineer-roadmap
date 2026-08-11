import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from src.services.rag_service import rag_answer

async def test():
    result = await rag_answer("监督学习和无监督学习有什么区别？")
    print(f"答案: {result['answer']}")
    print(f"来源: {len(result['sources'])} 个文档块")
    print(f"是否找到答案: {result['has_answer']}")

if __name__ == "__main__":
    asyncio.run(test())