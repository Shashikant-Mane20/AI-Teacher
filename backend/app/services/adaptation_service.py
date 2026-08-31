class AdaptationService:
    async def adapt_for_student(self, learner_level: str, previous_answers: list):
        if learner_level == "beginner":
            return {
                "difficulty": "easy",
                "explanation_style": "simple examples and analogies",
            }
        if learner_level == "advanced":
            return {
                "difficulty": "hard",
                "explanation_style": "technical details and examples",
            }
        return {
            "difficulty": "medium",
            "explanation_style": "balanced explanation",
        }
