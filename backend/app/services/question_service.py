class QuestionService:
    async def generate_question(self, concept: str, level: str):
        return {
            "concept": concept,
            "type": "mcq",
            "prompt": f"Which statement best explains {concept}?",
            "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
            "expected_answer": "B. Option 2",
            "difficulty": level,
        }
