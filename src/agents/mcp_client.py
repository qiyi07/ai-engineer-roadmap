import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_mcp_client():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["src/agents/mcp_server.py"],
    )

    print("🔌 正在启动 MCP Server...")
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 增加超时，避免无限等待
                await asyncio.wait_for(session.initialize(), timeout=10.0)
                print("✅ 连接成功！")

                tools = await session.list_tools()
                print(f"📦 可用工具: {[t.name for t in tools.tools]}")

                result = await session.call_tool("ping", {})
                print(f"🏓 响应: {result.content[0].text}")

    except asyncio.TimeoutError:
        print("❌ 连接超时，请检查 Server 是否正常启动")
    except Exception as e:
        print(f"❌ 错误: {e}")

if __name__ == "__main__":
    asyncio.run(run_mcp_client())