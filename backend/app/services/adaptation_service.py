class AdaptationService:
    async def adapt_for_student(self, learner_level: str, previous_answers: list):
        incorrect_answers = sum(not answer.get("is_correct", False) for answer in previous_answers)
        if incorrect_answers >= 2:
            return {
                "action": "SIMPLIFY + GIVE_ANALOGY",
                "difficulty": "easy",
                "explanation_style": "simple examples and analogies",
                "retest": True,
            }
        if incorrect_answers == 1:
            return {
                "action": "REEXPLAIN + ANALOGY",
                "difficulty": "easy",
                "explanation_style": "water-pipe analogy and simple example",
                "retest": True,
            }
        if learner_level == "beginner":
            return {
                "action": "CONTINUE",
                "difficulty": "easy",
                "explanation_style": "simple examples and analogies",
                "retest": False,
            }
        if learner_level == "advanced":
            return {
                "action": "INCREASE_DIFFICULTY",
                "difficulty": "hard",
                "explanation_style": "technical details and examples",
                "retest": False,
            }
        return {
            "action": "CONTINUE",
            "difficulty": "medium",
            "explanation_style": "balanced explanation",
            "retest": False,
        }
