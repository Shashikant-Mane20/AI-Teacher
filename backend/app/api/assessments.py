from fastapi import APIRouter

from app.schemas.assessment import AssessmentReport, AssessmentRequest

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post("/generate", response_model=AssessmentReport)
async def generate_assessment(payload: AssessmentRequest):
    return {
        "student_id": payload.student_id,
        "lesson_id": payload.lesson_id,
        "score": 80.0,
        "strong_areas": ["current", "voltage"],
        "weak_areas": ["resistance", "ohm's law"],
        "recommendations": [
            "Revise Ohm's Law",
            "Practice two more verbal problem sets",
        ],
        "next_topic": "Electricity basics",
    }
