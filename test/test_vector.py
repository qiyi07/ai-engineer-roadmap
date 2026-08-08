from src.rag.text_splitter import split_text

long_text = """这是第一段。这是第二段。这是第三段，内容更长一些。"""
chunks = split_text(long_text, chunk_size=50, chunk_overlap=10)
for c in chunks:
    print(f"块 {c['index']}: {c['content'][:30]}...")