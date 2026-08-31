from pydantic import BaseModel
from typing import Optional, List


class QuestionCreateRequest(BaseModel):
    lesson_id: str
    concept: str
    question_type: str = "mcq"


class Question(BaseModel):
    id: str
    lesson_id: str
    concept: str
    question_type: str
    prompt: str
    options: Optional[List[str]] = None
    expected_answer: Optional[str] = None
    difficulty: str = "medium"


class EvaluateAnswerRequest(BaseModel):
    lesson_id: str
    question_id: str
    student_answer: str


class EvaluateAnswerResponse(BaseModel):
    is_correct: bool
    score: float
    explanation: str
    misconception_detected: bool
    misconception: Optional[str]
    next_action: str
