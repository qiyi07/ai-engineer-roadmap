"""
MCP 最小演示：模拟一个 MCP Server，提供文件读取和计算器工具。
用简单的函数模拟概念。
"""
import json

class MCPServer:
    """模拟 MCP Server"""
    
    def __init__(self):
        self.tools = {
            "read_file": self.read_file,
            "calculate": self.calculate,
        }
    
    def read_file(self, path: str) -> str:
        """模拟读取文件"""
        return f"[MCP] 读取文件 {path} 的内容：这是模拟的文件内容。"
    
    def calculate(self, expression: str) -> float:
        """执行计算"""
        return eval(expression)
    
    def handle_request(self, request: dict) -> dict:
        """处理 MCP 请求"""
        tool_name = request.get("tool")
        params = request.get("params", {})
        if tool_name in self.tools:
            result = self.tools[tool_name](**params)
            return {"status": "success", "result": result}
        return {"status": "error", "message": "Tool not found"}

# 演示
if __name__ == "__main__":
    server = MCPServer()
    # 模拟客户端请求
    req = {"tool": "calculate", "params": {"expression": "25 * 4 + 10"}}
    resp = server.handle_request(req)
    print(f"📡 MCP 响应: {resp}")