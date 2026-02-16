from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Question, Answer
from schemas.schemas import AnswerCreate, AnswerResponse
from services.evaluation_service import evaluate_answer
from core.security import get_current_user

router = APIRouter(prefix="/answers", tags=["Answers"])

@router.post("/{question_id}", response_model=AnswerResponse)
def submit_answer(
    question_id: int,
    payload: AnswerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    existing = db.query(Answer).filter(
        Answer.question_id == question_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Answer already submitted for this question"
        )

    answer = Answer(
        question_id=question.id,
        user_answer=payload.user_answer,
        score=0,
        feedback="Evaluating..."
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    score, feedback = evaluate_answer(
        payload.user_answer,
        question.content
    )
    answer.score = score
    answer.feedback = feedback
    db.commit()

    total_questions = db.query(Question).filter(
        Question.interview_id == question.interview_id
    ).count()

    answered = db.query(Answer).join(Question).filter(
        Question.interview_id == question.interview_id
    ).count()

    if total_questions == answered:
         interview = question.interview
         interview.is_completed = True

    # 🔹 Collect all answers
         all_answers = (
             db.query(Answer)
            .join(Question)
            .filter(Question.interview_id == interview.id)
            .all()
         )

         all_answers_text = [a.user_answer for a in all_answers]

    # 🔹 Generate overall verdict (MATCHES YOUR FUNCTION)
         from services.evaluation_service import evaluate_overall
         overall_verdict = evaluate_overall(all_answers_text)
         interview.overall_verdict = overall_verdict
         db.commit()
    return answer

@router.get("/interview/{interview_id}")
def get_answers_for_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    answers = (
        db.query(Answer)
        .join(Question)
        .filter(Question.interview_id == interview_id)
        .all()
    )

    return answers
