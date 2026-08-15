import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from typing import List, Optional, Dict, Any
from functools import lru_cache
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

# ---------- 默认 Collection ----------
DEFAULT_COLLECTION = getattr(settings, "vector_collection_default", "docs")

# ---------- Collection 缓存 ----------
_collection_cache: Dict[str, PGVector] = {}


def get_vector_store(collection_name: str = DEFAULT_COLLECTION) -> PGVector:
    """
    获取指定 collection 的 PGVector 实例（带缓存）
    不同 collection 对应不同的表，用于多知识库隔离
    """
    if collection_name not in _collection_cache:
        _collection_cache[collection_name] = PGVector(
            connection_string=CONNECTION_STRING,
            embedding_function=embeddings,
            collection_name=collection_name,
            use_jsonb=True,
        )
    return _collection_cache[collection_name]


# ---------- 默认 Collection 操作（向后兼容） ----------
def _get_default_store() -> PGVector:
    """获取默认 collection 的实例"""
    return get_vector_store(DEFAULT_COLLECTION)


def add_documents(texts: List[str], metadatas: Optional[List[dict]] = None) -> List[str]:
    """直接存入文本列表（使用默认 collection）"""
    if metadatas is None:
        metadatas = [{}] * len(texts)
    return _get_default_store().add_texts(texts, metadatas=metadatas)


def search(query: str, top_k: int = 3) -> List[dict]:
    """向量检索（使用默认 collection）"""
    results = _get_default_store().similarity_search_with_score(query, k=top_k)
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
    """向量检索 + 阈值过滤（使用默认 collection）"""
    results = _get_default_store().similarity_search_with_score(query, k=top_k)
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
    """清空默认 collection（谨慎使用）"""
    _get_default_store().delete_collection()


# ---------- 多 Collection 操作 ----------
def add_documents_to_collection(
    texts: List[str],
    collection_name: str,
    metadatas: Optional[List[dict]] = None,
) -> List[str]:
    """向指定 collection 存入文本列表"""
    if metadatas is None:
        metadatas = [{}] * len(texts)
    store = get_vector_store(collection_name)
    return store.add_texts(texts, metadatas=metadatas)


def search_in_collection(
    query: str,
    collection_name: str,
    top_k: int = 3,
    score_threshold: Optional[float] = None,
) -> List[dict]:
    """
    在指定 collection 中检索
    如果提供 score_threshold，则过滤低于阈值的结果
    """
    store = get_vector_store(collection_name)
    results = store.similarity_search_with_score(query, k=top_k)
    
    items = [
        {
            "content": doc.page_content,
            "score": score,
            "metadata": doc.metadata,
        }
        for doc, score in results
    ]
    
    if score_threshold is not None:
        items = [item for item in items if item["score"] >= score_threshold]
    
    return items


def delete_collection_by_name(collection_name: str) -> None:
    """删除指定 collection"""
    store = get_vector_store(collection_name)
    store.delete_collection()
    # 从缓存中移除
    if collection_name in _collection_cache:
        del _collection_cache[collection_name]


def list_collections() -> List[str]:
    """
    列出所有 collection（通过查询 PGVector 元数据表）
    注意：此操作需要直接查询数据库，PGVector 没有直接提供 API
    这里返回缓存中的 collection 列表
    """
    return list(_collection_cache.keys())


# ---------- 扩展功能：元数据 + 切分入库 ----------
def add_document_with_metadata(
    content: str,
    source: str,
    page: Optional[int] = None,
    collection_name: str = DEFAULT_COLLECTION,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[str]:
    """
    将单个文档切分后入库到指定 collection，附带元数据
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
    store = get_vector_store(collection_name)
    return store.add_texts(texts, metadatas=metadatas)


def add_documents_batch(
    documents: List[Dict[str, Any]],
    collection_name: str = DEFAULT_COLLECTION,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> List[str]:
    """
    批量入库多个文档到指定 collection
    documents: [{"content": "...", "source": "file1.md", "page": 1}, ...]
    """
    all_ids = []
    for doc in documents:
        ids = add_document_with_metadata(
            content=doc["content"],
            source=doc.get("source", "unknown"),
            page=doc.get("page"),
            collection_name=collection_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        all_ids.extend(ids)
    return all_ids


# ---------- 缓存检索 ----------
@lru_cache(maxsize=128)
def cached_search(query: str, top_k: int = 3, collection_name: str = DEFAULT_COLLECTION) -> List[dict]:
    """带缓存的检索（用于高频相似查询）"""
    return search_in_collection(query, collection_name, top_k)


# ---------- 集合操作辅助 ----------
def get_collection_size(collection_name: str) -> int:
    """
    获取指定 collection 中的文档块数量
    注意：此操作需要额外查询，仅作为辅助
    """
    store = get_vector_store(collection_name)
    # PGVector 没有直接提供 count 方法，通过查询元数据表实现
    # 这里简化实现：通过检索空字符串获取部分结果
    try:
        results = store.similarity_search_with_score("", k=1)
        return len(results)  # 不准确，仅作示意
    except:
        return 0


def ensure_collection_exists(collection_name: str) -> bool:
    """
    确保 collection 存在（通过获取实例并执行空操作）
    """
    try:
        store = get_vector_store(collection_name)
        # 执行一个空检索来验证
        store.similarity_search_with_score("test", k=1)
        return True
    except Exception:
        return False