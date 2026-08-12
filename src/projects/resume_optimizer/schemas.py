from pydantic import BaseModel, Field
from typing import List, Optional

class Education(BaseModel):
    school: str
    major: str
    degree: str  # 本科/硕士/博士
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class WorkExperience(BaseModel):
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: str
    achievements: List[str] = Field(default_factory=list)

class Skill(BaseModel):
    name: str
    level: Optional[str] = "熟悉"  # 熟悉/掌握/精通

class Resume(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    summary: str
    education: List[Education] = Field(default_factory=list)
    experience: List[WorkExperience] = Field(default_factory=list)
    skills: List[Skill] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)

class JDInput(BaseModel):
    title: str
    company: Optional[str] = None
    description: str
    requirements: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)

class MatchAnalysis(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    skill_match_rate: float  # 0-1
    experience_match: str  # "匹配"/"部分匹配"/"不匹配"
    missing_skills: List[str]
    highlight_strengths: List[str]
    suggestion: str
    recommend_apply: bool