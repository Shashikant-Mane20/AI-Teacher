from typing import Any, Dict

from app.services.llm_service import LLMService


class TeacherService:
    def __init__(self):
        self.llm = LLMService()

    async def create_lesson_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        topic = payload.get("topic")
        learner_level = payload.get("learner_level", "beginner")
        language = payload.get("language", "en")
        time_minutes = payload.get("available_time_minutes", 20)

        ai_plan = await self.llm.generate_json(
            "You are an adaptive teacher. Return only valid JSON with keys: objectives, questions_to_ask, assessment_plan, visual_plan. Each objective needs concept, explanation, example, visual_type.",
            f"Create a {time_minutes}-minute {learner_level} lesson in {language} about {topic}. Learning goal: {payload.get('learning_goal') or 'understand the topic'}. Source material: {payload.get('source_context') or 'none'}.",
        )
        if ai_plan and all(key in ai_plan for key in ("objectives", "questions_to_ask", "assessment_plan", "visual_plan")):
            return {
                "topic": topic,
                "level": learner_level,
                "language": language,
                "duration_minutes": time_minutes,
                **ai_plan,
            }

        return {
            "topic": topic,
            "level": learner_level,
            "language": language,
            "duration_minutes": time_minutes,
            "objectives": [
                {
                    "concept": "Introduction",
                    "explanation": f"Explain {topic} in a clear and structured way.",
                    "example": "Use a real-world analogy.",
                    "visual_type": "diagram",
                }
            ],
            "questions_to_ask": [
                "Can you explain this in your own words?",
                "Which part feels difficult?",
            ],
            "assessment_plan": ["MCQ quiz", "concept check", "final recap"],
            "visual_plan": ["diagram", "formula", "chart"],
        }

    async def evaluate_answer(self, student_answer: str, expected_answer: str) -> Dict[str, Any]:
        is_correct = student_answer.lower().strip() == expected_answer.lower().strip()
        if is_correct:
            return {
                "is_correct": True,
                "score": 1.0,
                "explanation": "Good job. You understood the concept.",
                "misconception_detected": False,
                "misconception": None,
                "next_action": "Continue to the next concept.",
            }

        return {
            "is_correct": False,
            "score": 0.0,
            "explanation": "You are close, but the concept is slightly different.",
            "misconception_detected": True,
            "misconception": "You may be confusing the main idea with a related idea.",
            "next_action": "Explain the concept again using a simpler example.",
        }
