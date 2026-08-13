import json
from langchain_core.messages import HumanMessage, SystemMessage
from src.services.llm_service import chat_with_llm_complete
from src.projects.resume_optimizer.schemas import Resume, MatchAnalysis
from src.projects.resume_optimizer.prompts import RESUME_PARSING_PROMPT, JD_ANALYSIS_PROMPT
from src.projects.resume_optimizer.schemas import TailoredCVResponse
from src.projects.resume_optimizer.prompts import TAILORED_CV_PROMPT
async def parse_resume(resume_text: str) -> Resume:
    """解析简历文本为结构化 Resume 对象"""
    prompt = RESUME_PARSING_PROMPT.format(resume_text=resume_text)
    response = await chat_with_llm_complete(
        user_message=prompt,
        system_prompt="你是一个专业的简历解析助手，只输出 JSON，不要有其他内容。",
        temperature=0.1,
    )
    # 清理可能包含的 markdown 代码块
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    if response.endswith("```"):
        response = response[:-3]
    data = json.loads(response.strip())
    return Resume(**data)

async def analyze_jd(jd_text: str, resume: Resume) -> MatchAnalysis:
    """分析职位与简历的匹配度"""
    prompt = JD_ANALYSIS_PROMPT.format(
        jd_text=jd_text,
        resume_json=resume.model_dump_json(indent=2),
    )
    response = await chat_with_llm_complete(
        user_message=prompt,
        system_prompt="你是一个专业的招聘分析助手，只输出 JSON，不要有其他内容。",
        temperature=0.2,
    )
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    if response.endswith("```"):
        response = response[:-3]
    data = json.loads(response.strip())
    return MatchAnalysis(**data)



async def tailor_cv(resume: Resume, jd_text: str) -> TailoredCVResponse:
    """根据 JD 定制化简历"""
    prompt = TAILORED_CV_PROMPT.format(
        resume_json=resume.model_dump_json(indent=2),
        jd_text=jd_text,
    )
    response = await chat_with_llm_complete(
        user_message=prompt,
        system_prompt="你是一个专业的简历优化助手，只输出 JSON，不要有其他内容。",
        temperature=0.3,
    )
    # 清理 JSON
    response = response.strip()
    if response.startswith("```json"):
        response = response[7:]
    if response.endswith("```"):
        response = response[:-3]
    data = json.loads(response.strip())
    return TailoredCVResponse(**data)