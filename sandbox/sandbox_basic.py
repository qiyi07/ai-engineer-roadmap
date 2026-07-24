"""
# 列表 / 字典推导式
# 场景：清洗 RAG 召回的原始文档列表
raw_docs = [
    {"content": "  Python is great  ", "score": 0.9},
    {"content": "  FastAPI is fast  ", "score": None},   # 脏数据
    {"content": "  Pydantic rocks  ", "score": 0.8},
]

# 推导式：过滤掉 score 为 None 的，并且去除 content 首尾空格
cleaned = [
    doc["content"].strip() 
    for doc in raw_docs 
    if doc.get("score") is not None
]
print(cleaned)  # 输出: ['Python is great', 'Pydantic rocks']
"""

# try/except 细粒度捕获（区分错误类型）
import json

# 模拟调用第三方 LLM API 返回的异常格式
responses = [
    '{"answer": "ok"}',
    'not a json',
    '{"answer": null}'   # 业务返回空
]

for idx, resp in enumerate(responses):
    try:
        data = json.loads(resp)
        print(f"第{idx}条: {data['answer']}")
    except json.JSONDecodeError as e:
        print(f"第{idx}条 JSON 解析失败: {e}")
    except KeyError as e:
        print(f"第{idx}条 缺少 answer 字段: {e}")


# with open 文件操作 + 异常安全
# 写一个临时文件
with open("test.txt", "w", encoding="utf-8") as f:
    f.write("Hello AI Engineer")

# 读文件（如果文件不存在，触发 FileNotFoundError）
try:
    with open("missing.txt", "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("⚠️ 文件不存在，跳过读取")