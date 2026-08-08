from typing import List, Dict, Any, Optional
from pathlib import Path

# 文本文件加载
def load_txt(file_path: str) -> str:
    """加载纯文本文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Markdown 加载（保留标题结构）
def load_markdown(file_path: str) -> str:
    """加载 Markdown 文件，保留基本格式"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content

# PDF 加载（需要 pypdf 或 pypdf2）
try:
    from pypdf import PdfReader
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    print("pypdf 未安装，PDF 加载功能不可用。执行: uv add pypdf")

def load_pdf(file_path: str) -> str:
    """加载 PDF 文件，提取所有文本"""
    if not HAS_PDF:
        raise ImportError("pypdf 未安装，请执行: uv add pypdf")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# 自动检测并加载
def load_document(file_path: str) -> str:
    """根据文件扩展名自动选择加载器"""
    ext = Path(file_path).suffix.lower()
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".md":
        return load_markdown(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")