class VideoService:
    async def build_video_plan(self, lesson_title: str, visual_plan: list):
        return {
            "title": lesson_title,
            "scene_order": visual_plan,
            "speech_ready": True,
            "avatar_required": True,
            "render_status": "queued",
        }
