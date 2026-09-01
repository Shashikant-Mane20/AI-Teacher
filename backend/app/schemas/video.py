from pydantic import BaseModel


class VideoGenerateRequest(BaseModel):
    lesson_id: str
    lesson_title: str
    visual_plan: list[str] = []
    language: str = "en"


class VideoPlanResponse(BaseModel):
    lesson_id: str
    title: str
    scene_order: list[str]
    speech_ready: bool
    avatar_required: bool
    voice_language: str
    render_status: str
