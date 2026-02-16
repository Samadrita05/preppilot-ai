from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import Interview
from schemas.schemas import InterviewCreate, InterviewResponse
from core.security import get_current_user

router = APIRouter(prefix="/interviews", tags=["Interviews"])

@router.post("/", response_model=InterviewResponse)
def create_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_interview = Interview(
        role=interview.role,
        difficulty=interview.difficulty,
        user_id=current_user.id,
        is_completed=False
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview


@router.get("/", response_model=list[InterviewResponse])
def get_my_interviews(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    interviews = db.query(Interview).filter(
        Interview.user_id == current_user.id
    ).all()

    for interview in interviews:
       if interview.is_completed is None:
        interview.is_completed = False

    return interviews

@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
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
    
    if interview.is_completed is None:
        interview.is_completed = False

    return interview
