import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.projects.resume_optimizer.service import parse_resume, analyze_jd

async def test():
    resume_text = """
    张三
    zhangsan@email.com
    13800138000

    5年 Python 后端开发经验，擅长 FastAPI 和微服务架构。
    
    教育经历：
    xx大学 - 计算机科学与技术 - 本科 - 2015-2019
    
    工作经历：
    xxxx - 后端开发工程师 - 2019-2022
    负责 AI 中台服务开发，日请求量 1000 万+
    
    技能：
    Python (精通), FastAPI (精通), Docker (掌握), PostgreSQL (掌握)
    """
    
    jd_text = """
    职位：Python 后端开发工程师
    公司：x科技公司
    
    职责：
    1. 负责 AI 产品后端服务开发
    2. 参与系统架构设计
    
    要求：
    1. 3 年以上 Python 开发经验
    2. 熟悉 FastAPI 或 Django
    3. 熟悉 PostgreSQL
    4. 有 Docker/K8s 经验
    
    加分项：
    1. 有 AI 相关项目经验
    """
    
    resume = await parse_resume(resume_text)
    print(f"解析简历成功: {resume.name}")
    
    result = await analyze_jd(jd_text, resume)
    print(f"匹配度: {result.overall_score}%")
    print(f"建议: {result.suggestion}")
    print(f"推荐投递: {result.recommend_apply}")

if __name__ == "__main__":
    asyncio.run(test())