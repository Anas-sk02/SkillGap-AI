from pydantic import BaseModel
from typing import List, Optional, Dict


class StudentProfile(BaseModel):
    student_id: Optional[str] = None
    current_skills: List[str]
    target_role: str
    projects: List[str] = []
    experience_level: str


class MissingSkill(BaseModel):
    skill: str
    weight: float
    stage: str
    reason: str


class SkillGapResponse(BaseModel):
    student_id: Optional[str]
    target_role: str
    match_percentage: float
    missing_skills: List[MissingSkill]
    present_skills: List[str]


class RoadmapStageSkill(BaseModel):
    skill: str
    weight: float
    reason: str


class RoadmapResponse(BaseModel):
    target_role: str
    roadmap: Dict[str, List[RoadmapStageSkill]]


class RoleSkillDetail(BaseModel):
    name: str
    stage: str
    weight: float


class RoleDetail(BaseModel):
    role: str
    skills: List[RoleSkillDetail]


class RolesCatalogueResponse(BaseModel):
    roles: List[RoleDetail]


class ProgressUpdate(BaseModel):
    student_id: str
    target_role: str
    completed_skills: List[str]


class ProgressResponse(BaseModel):
    student_id: str
    target_role: str
    completed_skills: List[str]
    total_roadmap_skills: int
    completion_percentage: float
