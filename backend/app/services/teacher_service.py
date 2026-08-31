from typing import Any, Dict


class TeacherService:
    async def create_lesson_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        topic = payload.get("topic")
        learner_level = payload.get("learner_level", "beginner")
        language = payload.get("language", "en")
        time_minutes = payload.get("available_time_minutes", 20)

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
