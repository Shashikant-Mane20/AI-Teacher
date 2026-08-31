from fastapi import APIRouter

from app.schemas.student import StudentProfile, StudentProfileCreate

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/create", response_model=StudentProfile)
async def create_student(payload: StudentProfileCreate):
    return {
        "id": "student_001",
        "name": payload.name,
        "level": payload.level,
        "preferred_language": payload.preferred_language,
        "learning_goal": payload.learning_goal,
        "strong_concepts": ["basic logic"],
        "weak_concepts": ["advanced examples"],
        "progress_score": 0.0,
    }


@router.get("/{student_id}/profile", response_model=StudentProfile)
async def get_student_profile(student_id: str):
    return {
        "id": student_id,
        "name": "Demo Student",
        "level": "beginner",
        "preferred_language": "hi",
        "learning_goal": "Understand basics",
        "strong_concepts": ["simple examples"],
        "weak_concepts": ["complex formulas"],
        "progress_score": 72.5,
    }
