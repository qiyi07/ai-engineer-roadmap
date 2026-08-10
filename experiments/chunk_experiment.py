import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import os
from src.rag.evaluator import load_eval_data, evaluate_retrieval
from src.rag.vector_store import add_documents
from src.rag.document_loader import load_document
from src.rag.text_splitter import split_text

def run_chunk_experiment():
    # 设置 HuggingFace 镜像（解决 SSL 证书问题）
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    
    # 加载文档
    content = load_document("sample.txt")
    eval_data = load_eval_data()
    
    # 实验参数组合
    configs = [
        {"size": 200, "overlap": 20},
        {"size": 500, "overlap": 50},
        {"size": 800, "overlap": 80},
        {"size": 1000, "overlap": 100},
    ]
    
    results = []
    for cfg in configs:
        print(f"正在测试 chunk_size={cfg['size']}, overlap={cfg['overlap']} ...")
        # 1. 切分文档
        chunks = split_text(content, cfg["size"], cfg["overlap"])
        texts = [c["content"] for c in chunks]
        metadatas = [{"source": "sample.txt", "chunk_index": c["index"]} for c in chunks]
        
        # 2. 入库（注意：每次实验会追加数据，不重复清空，仅用于演示趋势）
        ids = add_documents(texts, metadatas=metadatas)
        print(f"  入库 {len(ids)} 个块")
        
        # 3. 评估
        eval_result = evaluate_retrieval(
            eval_data,
            chunk_size=cfg["size"],
            chunk_overlap=cfg["overlap"],
            top_k=3,
        )
        results.append({
            "chunk_size": cfg["size"],
            "chunk_overlap": cfg["overlap"],
            "recall": eval_result["recall"],
            "avg_results": eval_result["avg_results"],
        })
    
    # 输出对比
    print("\n📊 Chunk 大小实验对比")
    print("-" * 50)
    for r in results:
        print(f"size={r['chunk_size']}, overlap={r['chunk_overlap']} -> 召回率: {r['recall']:.2%}")
    
    if results:
        best = max(results, key=lambda x: x["recall"])
        print(f"\n✅ 最佳配置: chunk_size={best['chunk_size']}, overlap={best['chunk_overlap']}, 召回率={best['recall']:.2%}")

if __name__ == "__main__":
    run_chunk_experiment()