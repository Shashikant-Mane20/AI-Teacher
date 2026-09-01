from fastapi import APIRouter

from app.schemas.assessment import AssessmentReport, AssessmentRequest
from app.api.interactive import get_lesson_attempts
from app.services.assessment_service import AssessmentService

router = APIRouter(prefix="/assessments", tags=["assessments"])
assessment_service = AssessmentService()


@router.post("/generate", response_model=AssessmentReport)
async def generate_assessment(payload: AssessmentRequest):
    attempts = get_lesson_attempts(payload.lesson_id)
    report = await assessment_service.create_report_from_attempts(attempts)
    return {
        "student_id": payload.student_id,
        "lesson_id": payload.lesson_id,
        **report,
    }
