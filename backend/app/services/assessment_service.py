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

    async def create_report_from_attempts(self, attempts: list):
        if not attempts:
            return await self.create_report(0.0, [], ["No completed questions"])
        score = round(sum(attempt["score"] for attempt in attempts) / len(attempts), 1)
        concepts = {attempt["concept"] for attempt in attempts}
        strong_areas = sorted({attempt["concept"] for attempt in attempts if attempt["is_correct"]})
        weak_areas = sorted(concepts - set(strong_areas))
        return await self.create_report(score, strong_areas, weak_areas)
