import asyncio
import random
from src.utils.logger import logger

async def call_llm_api(task_id: int, semaphore: asyncio.Semaphore):
    """模拟调用 LLM API，每次耗时 1~2 秒"""
    async with semaphore:  # 获取信号量，如果并发数已满则等待
        logger.info(f"任务 {task_id} 开始调用 API...")
        await asyncio.sleep(random.uniform(1.0, 2.0))  # 模拟网络 IO
        result = f"任务 {task_id} 的回复"
        logger.info(f"任务 {task_id} 完成")
        return result

async def main():
    # 限制最大并发数为 3（模拟 API 的并发上限）
    semaphore = asyncio.Semaphore(3)
    
    # 同时发起 10 个任务
    tasks = [call_llm_api(i, semaphore) for i in range(10)]
    
    logger.info("🚀 开始并发请求（限流 3）")
    results = await asyncio.gather(*tasks)
    logger.info(f"全部完成，共 {len(results)} 个结果")

if __name__ == "__main__":
    asyncio.run(main())