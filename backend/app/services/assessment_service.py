class AssessmentService:
    async def create_report(self, score: float, strong_areas: list, weak_areas: list):
        return {
            "score": score,
            "strong_areas": strong_areas,
            "weak_areas": weak_areas,
            "recommendations": [
                "Revise weak concepts",
                "Practice 3 short application questions",
            ],
            "next_topic": "Continue with the next concept",
        }
