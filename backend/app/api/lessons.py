from fastapi import APIRouter

from app.schemas.lesson import LessonCreateRequest, LessonResponse

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.post("/create", response_model=LessonResponse)
async def create_lesson(payload: LessonCreateRequest):
    lesson_id = "lesson_001"
    plan = {
        "lesson_id": lesson_id,
        "topic": payload.topic,
        "level": payload.learner_level,
        "language": payload.language,
        "duration_minutes": payload.available_time_minutes,
        "objectives": [
            {
                "concept": "Core concept",
                "explanation": f"Explain {payload.topic} in a clear and simple way.",
                "example": "Use a real-world example.",
                "visual_type": "diagram",
            }
        ],
        "questions_to_ask": [
            "Can you explain this in your own words?",
            "Which part feels difficult?",
        ],
        "assessment_plan": [
            "MCQ quiz",
            "short answer check",
            "final recap",
        ],
        "visual_plan": ["diagram", "formula", "chart"],
    }

    return {"lesson_id": lesson_id, "status": "created", "plan": plan}


@router.get("/{lesson_id}")
async def get_lesson(lesson_id: str):
    return {"lesson_id": lesson_id, "status": "ready"}


@router.post("/{lesson_id}/start")
async def start_lesson(lesson_id: str):
    return {"lesson_id": lesson_id, "status": "started"}


@router.post("/{lesson_id}/adapt")
async def adapt_lesson(lesson_id: str):
    return {"lesson_id": lesson_id, "status": "adapted"}
