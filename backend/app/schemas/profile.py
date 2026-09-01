from pydantic import BaseModel, Field


class StudentProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    educational_level: str = "other"
    preferred_language: str = "english"
    explanation_minutes: int = Field(default=20, ge=1, le=240)
    preferred_style: str = "beginner"
    progress: float = Field(default=0, ge=0, le=100)
    topics_studied: list[str] = []
    weak_concepts: list[str] = []
    learning_history: list[str] = []
    current_learning_path: list[str] = []


class StudentProfileResponse(StudentProfileUpdate):
    user_id: str
    email: str
