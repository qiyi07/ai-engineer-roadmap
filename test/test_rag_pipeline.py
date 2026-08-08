from src.rag.document_loader import load_document
from src.rag.vector_store import add_document_with_metadata, search

def test_full_pipeline():
    # 1. 加载文档
    content = load_document("sample.txt")
    print(f"原始文档长度: {len(content)} 字符")

    # 2. 切分并入库
    ids = add_document_with_metadata(
        content=content,
        source="sample.txt",
        chunk_size=300,
        chunk_overlap=30,
    )
    print(f"入库 {len(ids)} 个块")

    # 3. 检索测试
    query = "这个文档主要讲了什么？"
    results = search(query, top_k=2)
    for r in results:
        print(f"相似度: {r['score']:.4f}")
        print(f"内容: {r['content'][:80]}...")
        print(f"来源: {r['metadata']}")
        print("-" * 40)

if __name__ == "__main__":
    test_full_pipeline()