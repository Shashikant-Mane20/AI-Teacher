from fastapi import APIRouter

from app.schemas.video import VideoGenerateRequest, VideoPlanResponse
from app.services.video_service import VideoService

router = APIRouter(prefix="/video", tags=["video"])
video_service = VideoService()


@router.post("/generate", response_model=VideoPlanResponse)
async def generate_video_plan(payload: VideoGenerateRequest):
    plan = await video_service.build_video_plan(payload.lesson_title, payload.visual_plan)
    return {"lesson_id": payload.lesson_id, "voice_language": payload.language, **plan}
