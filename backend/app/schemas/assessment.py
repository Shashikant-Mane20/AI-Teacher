from pydantic import BaseModel
from typing import List, Optional


class AssessmentRequest(BaseModel):
    lesson_id: str
    student_id: str
    question_ids: List[str]


class AssessmentReport(BaseModel):
    student_id: str
    lesson_id: str
    score: float
    strong_areas: List[str]
    weak_areas: List[str]
    recommendations: List[str]
    next_topic: Optional[str]
