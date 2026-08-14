# src/agents/mcp_server.py（简化版）
import asyncio
import sys
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

server = Server("test-server")

@server.list_tools()
async def handle_list_tools():
    return [
        types.Tool(
            name="ping",
            description="返回 pong",
            inputSchema={"type": "object", "properties": {}},
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None):
    if name == "ping":
        return [types.TextContent(type="text", text="pong")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    # 打印启动日志，便于确认 Server 已运行
    print("MCP Server starting...", file=sys.stderr)
    async with mcp.server.stdio.stdio_server() as (read, write):
        await server.run(
            read,
            write,
            InitializationOptions(
                server_name="test-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())