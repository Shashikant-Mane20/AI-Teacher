from fastapi import APIRouter, HTTPException

from app.schemas.question import (
    EvaluateAnswerRequest,
    EvaluateAnswerResponse,
    Question,
    QuestionCreateRequest,
)
from app.services.adaptation_service import AdaptationService
from app.services.question_service import QuestionService

router = APIRouter(prefix="/lessons", tags=["interactive teaching"])
question_service = QuestionService()
adaptation_service = AdaptationService()
questions: dict[str, dict] = {}


@router.post("/{lesson_id}/question", response_model=Question)
async def create_question(lesson_id: str, payload: QuestionCreateRequest):
    if payload.lesson_id != lesson_id:
        raise HTTPException(status_code=400, detail="Lesson IDs do not match")

    question_data = await question_service.generate_question(payload.concept, "medium")
    question = {
        "id": f"question_{len(questions) + 1:03d}",
        "lesson_id": lesson_id,
        "concept": payload.concept,
        "question_type": payload.question_type,
        "prompt": question_data["prompt"],
        "options": question_data["options"],
        "expected_answer": question_data["expected_answer"],
        "difficulty": question_data["difficulty"],
    }
    questions[question["id"]] = question
    return question


@router.post("/{lesson_id}/answer", response_model=EvaluateAnswerResponse)
async def submit_answer(lesson_id: str, payload: EvaluateAnswerRequest):
    if payload.lesson_id != lesson_id:
        raise HTTPException(status_code=400, detail="Lesson IDs do not match")

    question = questions.get(payload.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    expected = question["expected_answer"].strip().lower()
    received = payload.student_answer.strip().lower()
    is_correct = received == expected or received.startswith(expected[:1])
    misconception = None if is_correct else (
        f"The learner selected '{payload.student_answer}' instead of the expected concept answer."
    )
    return {
        "is_correct": is_correct,
        "score": 100.0 if is_correct else 0.0,
        "explanation": (
            "Correct. The answer matches the concept."
            if is_correct
            else f"Review the concept. The expected answer is {question['expected_answer']}."
        ),
        "misconception_detected": not is_correct,
        "misconception": misconception,
        "next_action": "CONTINUE" if is_correct else "REEXPLAIN + ANALOGY",
    }


@router.post("/{lesson_id}/evaluate", response_model=EvaluateAnswerResponse)
async def evaluate_answer(lesson_id: str, payload: EvaluateAnswerRequest):
    return await submit_answer(lesson_id, payload)


@router.post("/{lesson_id}/continue")
async def continue_lesson(lesson_id: str):
    strategy = await adaptation_service.adapt_for_student("beginner", [])
    return {
        "lesson_id": lesson_id,
        "status": "continued",
        "next_action": "CONTINUE",
        "strategy": strategy,
    }
