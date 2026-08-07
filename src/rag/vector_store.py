from typing import List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.core.config import settings

# 初始化 Embedding 模型
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},  # 有 GPU 可改为 "cuda"
)

# 连接字符串（与主项目共用）
CONNECTION_STRING = settings.database_url

# 初始化 PGVector 实例
vector_store = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name="docs",  # 集合名，相当于“表名”
    use_jsonb=True,
)


def add_documents(texts: List[str], metadatas: Optional[List[dict]] = None) -> List[str]:
    """将文本列表向量化并存入 PGVector"""
    if metadatas is None:
        metadatas = [{}] * len(texts)
    ids = vector_store.add_texts(texts, metadatas=metadatas)
    return ids


def search(query: str, top_k: int = 3) -> List[dict]:
    """向量检索：输入文本，返回最相似的 top_k 条结果"""
    results = vector_store.similarity_search_with_score(query, k=top_k)
    return [
        {
            "content": doc.page_content,
            "score": score,
            "metadata": doc.metadata,
        }
        for doc, score in results
    ]


def delete_collection() -> None:
    """清空当前集合"""
    vector_store.delete_collection()