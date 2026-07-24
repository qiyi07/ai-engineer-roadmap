import asyncio
import time

# ---------- 同步版本 ----------
def sync_task(name: str, delay: float):
    print(f"[同步] {name} 开始，等待 {delay}s")
    time.sleep(delay)   # 阻塞整个线程
    print(f"[同步] {name} 完成")
    return f"{name}_result"

# ---------- 异步版本 ----------
async def async_task(name: str, delay: float):
    print(f"[异步] {name} 开始，等待 {delay}s")
    await asyncio.sleep(delay)   # 非阻塞，让出控制权
    print(f"[异步] {name} 完成")
    return f"{name}_result"

if __name__ == "__main__":
    # 调用异步函数
    result = asyncio.run(async_task("task1", 1))
    print(f"异步结果: {result}")

async def main():
    # 同时发起 3 个异步任务（模拟同时请求 3 个 API）
    start = time.time()
    
    results = await asyncio.gather(
        async_task("A", 2),
        async_task("B", 1),
        async_task("C", 1.5),
    )
    
    end = time.time()
    print(f"并发总耗时: {end - start:.2f} 秒")
    print(f"结果: {results}")

if __name__ == "__main__":
    asyncio.run(main())