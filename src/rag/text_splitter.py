from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    separators: List[str] = ["\n\n", "\n", "。", "！", "？", " ", ""],
) -> List[Dict[str, Any]]:
    """
    将长文本切分为多个块
    返回: [{"content": "...", "index": 0, "chunk_size": 500}, ...]
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    return [
        {
            "content": chunk,
            "index": i,
            "chunk_size": len(chunk),
        }
        for i, chunk in enumerate(chunks)
    ]