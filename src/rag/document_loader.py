from typing import List, Dict, Any, Optional
from pathlib import Path
import json

# ---------- 文本文件加载 ----------
def load_txt(file_path: str) -> str:
    """加载纯文本文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------- Markdown 加载 ----------
def load_markdown(file_path: str) -> str:
    """加载 Markdown 文件，保留基本格式"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content


# ---------- PDF 加载 ----------
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


# ---------- DOCX 加载 ----------
try:
    from docx import Document
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False
    print("python-docx 未安装，DOCX 加载功能不可用。执行: uv add python-docx")

def load_docx(file_path: str) -> str:
    """加载 Word 文档（.docx），提取所有段落文本"""
    if not HAS_DOCX:
        raise ImportError("python-docx 未安装，请执行: uv add python-docx")
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])


# ---------- JSON 加载 ----------
def load_json(file_path: str) -> str:
    """加载 JSON 文件，转为可读的文本描述（便于向量化）"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 如果 JSON 是数组，逐条展示；如果是对象，递归展开
    if isinstance(data, list):
        return "\n".join([json.dumps(item, ensure_ascii=False) for item in data])
    else:
        return json.dumps(data, ensure_ascii=False, indent=2)


# ---------- 自动检测并加载 ----------
def load_document(file_path: str) -> str:
    """根据文件扩展名自动选择加载器"""
    ext = Path(file_path).suffix.lower()
    if ext == ".txt":
        return load_txt(file_path)
    elif ext == ".md":
        return load_markdown(file_path)
    elif ext == ".pdf":
        return load_pdf(file_path)
    elif ext == ".docx":
        return load_docx(file_path)
    elif ext == ".json":
        return load_json(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")