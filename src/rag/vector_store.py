from typing import List, Optional, Dict, Any
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.core.config import settings
from src.rag.text_splitter import split_text

# ---------- 初始化 Embedding 模型 ----------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},  # 有 GPU 可改 "cuda"
)

# ---------- 连接字符串 ----------
CONNECTION_STRING = settings.database_url

# ---------- 初始化 PGVector ----------
vector_store = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name="docs",
    use_jsonb=True,
)

# ---------- 基础操作 ----------
def add_documents(texts: List[str], metadatas: Optional[List[dict]] = None) -> List[str]:
    """直接存入文本列表（用于简单测试）"""
    if metadatas is None:
        metadatas = [{}] * len(texts)
    return vector_store.add_texts(texts, metadatas=metadatas)


def search(query: str, top_k: int = 3) -> List[dict]:
    """向量检索"""
    results = vector_store.similarity_search_with_score(query, k=top_k)
    return [
        {
            "content": doc.page_content,
            "score": score,
            "metadata": doc.metadata,
        }
        for doc, score in results
    ]

def search_with_threshold(
    query: str,
    top_k: int = 3,
    score_threshold: float = 0.5,
) -> List[dict]:
    """
    向量检索 + 阈值过滤
    返回结果中 score > score_threshold 的文档块
    """
    results = vector_store.similarity_search_with_score(query, k=top_k)
    filtered = [
        {
            "content": doc.page_content,
            "score": score,
            "metadata": doc.metadata,
        }
        for doc, score in results
        if score >= score_threshold
    ]
    return filtered


def delete_collection() -> None:
    """清空集合（谨慎使用）"""
    vector_store.delete_collection()


# ---------- 扩展功能：元数据 + 切分入库 ----------
def add_document_with_metadata(
    content: str,
    source: str,
    page: Optional[int] = None,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[str]:
    """
    将单个文档切分后入库，附带元数据
    返回所有 chunk 的 ID 列表
    """
    chunks = split_text(content, chunk_size, chunk_overlap)
    texts = [c["content"] for c in chunks]
    metadatas = [
        {
            "source": source,
            "page": page,
            "chunk_index": c["index"],
            "chunk_size": c["chunk_size"],
        }
        for c in chunks
    ]
    return vector_store.add_texts(texts, metadatas=metadatas)


def add_documents_batch(
    documents: List[Dict[str, Any]],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[str]:
    """
    批量入库多个文档（每个文档独立切分）
    documents: [{"content": "...", "source": "file1.md", "page": 1}, ...]
    """
    all_ids = []
    for doc in documents:
        ids = add_document_with_metadata(
            content=doc["content"],
            source=doc.get("source", "unknown"),
            page=doc.get("page"),
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        all_ids.extend(ids)
    return all_ids