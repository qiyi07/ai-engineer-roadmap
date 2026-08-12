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

请从以下维度评估：
1. 技能匹配率（0-1）
2. 经验匹配程度（匹配/部分匹配/不匹配）
3. 缺失的关键技能
4. 候选人的突出优势
5. 综合建议（50字内）
6. 是否推荐投递（是/否）

输出 JSON 格式。
"""