from fastapi import APIRouter

from app.schemas.lesson import LessonCreateRequest, LessonResponse
from app.api.documents import get_document_context
from app.services.video_service import VideoService
from app.services.teacher_service import TeacherService

router = APIRouter(prefix="/lessons", tags=["lessons"])
video_service = VideoService()
teacher_service = TeacherService()


@router.post("/create", response_model=LessonResponse)
async def create_lesson(payload: LessonCreateRequest):
    lesson_id = "lesson_001"
    document = get_document_context(payload.uploaded_document_id) if payload.uploaded_document_id else None
    document_text = document["text"] if document else ""
    topic = payload.topic
    if document and (not topic or topic.lower() in {"uploaded document", "document"}):
        topic = document["metadata"]["title"]
    source_hint = document_text[:500] if document_text else f"Explain {topic} in a clear and simple way."
    plan = await teacher_service.create_lesson_plan({
        **payload.model_dump(),
        "topic": topic,
        "source_context": source_hint,
    })
    plan["lesson_id"] = lesson_id

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
