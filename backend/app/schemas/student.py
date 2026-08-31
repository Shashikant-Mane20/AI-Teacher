from pydantic import BaseModel
from typing import Optional, List


class StudentProfileCreate(BaseModel):
    name: str
    level: str = "beginner"
    preferred_language: str = "en"
    learning_goal: Optional[str] = None


class StudentProfile(BaseModel):
    id: str
    name: str
    level: str
    preferred_language: str
    learning_goal: Optional[str]
    strong_concepts: List[str] = []
    weak_concepts: List[str] = []
    progress_score: float = 0.0
