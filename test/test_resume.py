import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.projects.resume_optimizer.service import parse_resume, analyze_jd, tailor_cv

# 把测试数据提取为全局变量（两个测试共用）
RESUME_TEXT = """
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

JD_TEXT = """
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


async def test_analyze():
    """测试简历解析 + JD 分析"""
    print("=" * 50)
    print("测试：简历解析 + JD 分析")
    print("=" * 50)
    
    resume = await parse_resume(RESUME_TEXT)
    print(f"解析简历成功: {resume.name}")
    print(f"   邮箱: {resume.email}")
    print(f"   技能: {', '.join([s.name for s in resume.skills])}")
    
    result = await analyze_jd(JD_TEXT, resume)
    print(f"\n匹配度: {result.overall_score}%")
    print(f"   技能匹配率: {result.skill_match_rate:.0%}")
    print(f"   经验匹配: {result.experience_match}")
    print(f"   缺失技能: {', '.join(result.missing_skills) if result.missing_skills else '无'}")
    print(f"   优势: {', '.join(result.highlight_strengths)}")
    print(f"   建议: {result.suggestion}")
    print(f"   推荐投递: {result.recommend_apply}")


async def test_tailor():
    """测试定制化简历生成"""
    print("\n" + "=" * 50)
    print("测试：定制化简历生成")
    print("=" * 50)
    
    resume = await parse_resume(RESUME_TEXT)
    result = await tailor_cv(resume, JD_TEXT)
    
    print(f"定制简历生成成功")
    print(f"\n个人简介:\n{result.summary}")
    print(f"\n核心技能: {', '.join(result.highlighted_skills)}")
    print(f"\n亮点成就:")
    for bullet in result.bullet_points[:3]:
        print(f"   • {bullet}")
    if len(result.bullet_points) > 3:
        print(f"   ... 还有 {len(result.bullet_points) - 3} 条")
    print(f"\n完整简历长度: {len(result.full_cv)} 字符")


async def main():
    await test_analyze()
    await test_tailor()


if __name__ == "__main__":
    asyncio.run(main())