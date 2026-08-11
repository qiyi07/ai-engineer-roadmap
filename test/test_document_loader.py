import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag.document_loader import load_document

def test_load_documents():
    """测试不同格式文档的加载"""
    files = [
        PROJECT_ROOT / "sample.txt",
        PROJECT_ROOT / "sample.md",
        PROJECT_ROOT / "sample.pdf",
    ]
    
    for file_path in files:
        if not file_path.exists():
            print(f"⚠️ 文件不存在: {file_path}")
            continue
        try:
            content = load_document(str(file_path))
            print(f"✅ {file_path.name}: {len(content)} 字符")
            preview = content[:100].replace("\n", " ")
            print(f"   预览: {preview}...\n")
        except Exception as e:
            print(f"❌ {file_path.name}: {e}\n")

if __name__ == "__main__":
    test_load_documents()