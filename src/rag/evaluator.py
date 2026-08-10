import json
from typing import List, Dict, Any
from src.rag.vector_store import search
from src.rag.text_splitter import split_text

def load_eval_data(file_path: str = "data/eval_queries.json") -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_retrieval(
    queries: List[Dict],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    top_k: int = 3,
    score_threshold: float = 0.5,
) -> Dict[str, Any]:
    """评估不同参数下的召回效果"""
    results = {
        "chunk_size": chunk_size,
        "chunk_overlap": chunk_overlap,
        "top_k": top_k,
        "score_threshold": score_threshold,
        "total_queries": len(queries),
        "hits": 0,
        "avg_results": 0,
        "details": []
    }
    
    for q in queries:
        query_text = q["query"]
        retrieved = search(query_text, top_k=top_k)
        # 检查是否命中预期来源
        expected = q.get("expected_sources", [])
        hit = any(
            any(exp in r["metadata"].get("source", "") for exp in expected)
            for r in retrieved
        )
        results["details"].append({
            "query": query_text,
            "hit": hit,
            "results_count": len(retrieved),
            "top_score": retrieved[0]["score"] if retrieved else 0
        })
        if hit:
            results["hits"] += 1
        results["avg_results"] += len(retrieved)
    
    results["recall"] = results["hits"] / results["total_queries"]
    results["avg_results"] /= results["total_queries"]
    return results