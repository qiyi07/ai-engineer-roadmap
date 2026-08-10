from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
import jieba
from src.rag.vector_store import vector_store

# 缓存 BM25 索引（简单实现，后续可优化）
_bm25_index = None
_all_texts = []

def build_bm25_index(chunks: List[Dict[str, Any]]):
    """构建 BM25 索引（全量文档）"""
    global _bm25_index, _all_texts
    _all_texts = [c["content"] for c in chunks]
    tokenized = [list(jieba.cut(text)) for text in _all_texts]
    _bm25_index = BM25Okapi(tokenized)

def bm25_search(query: str, top_k: int = 3) -> List[Dict]:
    """BM25 关键词检索"""
    if _bm25_index is None:
        return []
    tokenized_query = list(jieba.cut(query))
    scores = _bm25_index.get_scores(tokenized_query)
    # 获取 top_k 索引
    sorted_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [
        {
            "content": _all_texts[i],
            "score": scores[i],
            "type": "bm25"
        }
        for i in sorted_indices
    ]

def hybrid_search(query: str, top_k: int = 3, alpha: float = 0.5) -> List[Dict]:
    """
    混合检索：向量 + BM25
    alpha: 向量权重，BM25 权重为 1-alpha
    """
    # 向量检索
    vector_results = vector_store.similarity_search_with_score(query, k=top_k * 2)
    # BM25 检索
    bm25_results = bm25_search(query, top_k=top_k * 2)
    
    # 合并去重（基于内容）
    combined = {}
    for doc, score in vector_results:
        content = doc.page_content
        combined[content] = {
            "content": content,
            "vector_score": score,
            "bm25_score": 0,
            "metadata": doc.metadata,
        }
    for r in bm25_results:
        content = r["content"]
        if content in combined:
            combined[content]["bm25_score"] = r["score"]
        else:
            combined[content] = {
                "content": content,
                "vector_score": 0,
                "bm25_score": r["score"],
                "metadata": {},
            }
    
    # 计算综合分数（归一化）
    # 简单起见：直接加权求和（实际需归一化）
    results = []
    for content, data in combined.items():
        # 由于分数量级不同，这里简单相加（真实场景需归一化）
        combined_score = alpha * data["vector_score"] + (1 - alpha) * data["bm25_score"]
        results.append({
            "content": content,
            "score": combined_score,
            "metadata": data["metadata"],
        })
    
    # 排序并取 top_k
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]