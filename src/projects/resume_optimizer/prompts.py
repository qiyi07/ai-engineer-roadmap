RESUME_PARSING_PROMPT = """
你是一位专业的 HR 助理。请从以下简历文本中提取结构化信息。

简历内容：
{resume_text}

请以 JSON 格式输出，包含字段：name, email, phone, summary, education（列表，每项含 school, major, degree, start_date, end_date）, experience（列表，每项含 company, title, start_date, end_date, description, achievements）, skills（列表，含 name, level）, projects（列表）。
"""

JD_ANALYSIS_PROMPT = """
你是一位招聘专家。请分析以下职位描述，并与候选人简历进行匹配评估。

职位描述：
{jd_text}

候选人简历：
{resume_json}

请从以下维度评估，并输出 JSON 格式（只输出 JSON，不要有其他内容）：
- overall_score: 整数 (0-100)，综合匹配度
- skill_match_rate: 浮点数 (0-1)，技能匹配率
- experience_match: 字符串，"匹配"/"部分匹配"/"不匹配"
- missing_skills: 字符串列表，候选人缺失的关键技能
- highlight_strengths: 字符串列表，候选人的突出优势
- suggestion: 字符串，综合建议（50字内）
- recommend_apply: 布尔值，是否推荐投递

输出 JSON 示例：
{{
  "overall_score": 85,
  "skill_match_rate": 0.8,
  "experience_match": "部分匹配",
  "missing_skills": ["Kubernetes"],
  "highlight_strengths": ["Python 经验丰富", "AI 项目背景"],
  "suggestion": "候选人经验基本匹配，建议补充 K8s 技能后投递",
  "recommend_apply": true
}}
"""

TAILORED_CV_PROMPT = """
你是一位专业的简历顾问。请根据职位描述，对候选人的简历进行定制优化。

候选人简历：
{resume_json}

职位描述：
{jd_text}

优化要求：
1. 重写个人简介（summary），突出与岗位最相关的经验
2. 从技能中筛选出岗位最需要的 5 项，作为"核心技能"
3. 将工作经历中的成就重新表述，强调与岗位职责的关联
4. 生成完整定制版简历（包含所有章节）

输出 JSON 格式：
{{
  "summary": "定制后的个人简介",
  "highlighted_skills": ["技能1", "技能2", ...],
  "bullet_points": ["成就1", "成就2", ...],
  "full_cv": "完整简历文本"
}}
"""