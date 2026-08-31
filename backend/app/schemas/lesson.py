from pydantic import BaseModel
from typing import Optional, List


class LessonCreateRequest(BaseModel):
    topic: str
    learner_level: str = "beginner"
    language: str = "en"
    available_time_minutes: int = 20
    learning_goal: Optional[str] = None
    uploaded_document_id: Optional[str] = None
    teaching_style: str = "simple"


class LessonObjective(BaseModel):
    concept: str
    explanation: str
    example: str
    visual_type: str


class LessonPlan(BaseModel):
    lesson_id: str
    topic: str
    level: str
    language: str
    duration_minutes: int
    objectives: List[LessonObjective]
    questions_to_ask: List[str]
    assessment_plan: List[str]
    visual_plan: List[str]


class LessonResponse(BaseModel):
    lesson_id: str
    status: str
    plan: LessonPlan
