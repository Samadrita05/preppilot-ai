from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import Interview, Question
from services.question_service import generate_questions
from core.security import get_current_user
from schemas.schemas import QuestionGenerateResponse, QuestionResponse

router = APIRouter(prefix="/questions", tags=["Questions"])

@router.get("/single/{question_id}")
def get_single_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return {
        "id": question.id,
        "question_text": question.content,  # ⚠️ important
        "interview_id": question.interview_id,
    }

#  Generate Questions for an Interview
@router.post("/{interview_id}", response_model=QuestionGenerateResponse)
def generate_interview_questions(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    db.query(Question).filter(
        Question.interview_id == interview.id
    ).delete()
    db.commit()

    questions = generate_questions(
        interview.role,
        interview.difficulty
    )

    saved_questions = []
    for q in questions:
        question = Question(
            interview_id=interview.id,
            content=q
        )
        db.add(question)
        saved_questions.append(question)

    db.commit()

    return {
        "interview_id": interview.id,
        "questions": [
            QuestionResponse(id=q.id, question_text=q.content)
            for q in saved_questions
        ]
    }

# Get Questions for an Interview
@router.get("/{interview_id}", response_model=QuestionGenerateResponse)
def get_questions_for_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    questions = db.query(Question).filter(
        Question.interview_id == interview.id
    ).all()

    return {
        "interview_id": interview.id,
        "questions": [
            QuestionResponse(id=q.id, question_text=q.content)
            for q in questions
        ]
    }
