from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import Interview, Question, Answer
from schemas.schemas import InterviewReportResponse, ReportQuestion
from services.evaluation_service import evaluate_overall
from core.security import get_current_user
from utils.pdf_generator import generate_interview_pdf

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/interview/{interview_id}/pdf")
def download_interview_report_pdf(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    #  Verify interview ownership
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    if not interview.is_completed:
        raise HTTPException(
            status_code=400,
            detail="Interview not completed yet"
        )

    questions = (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .all()
    )

    all_answers_text = []
    for q in questions:
        ans = db.query(Answer).filter(
            Answer.question_id == q.id
        ).order_by(Answer.id.desc()).first()
        if ans:
            all_answers_text.append(ans.user_answer)

    #  SAME verdict as report page
    overall_verdict = interview.overall_verdict or "No overall evaluation available."


    pdf_buffer = generate_interview_pdf(
        interview=interview,
        questions=questions,
        overall_verdict=overall_verdict,
        db=db
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=interview_{interview_id}.pdf"
        }
    )

@router.get("/{interview_id}", response_model=InterviewReportResponse)
def get_interview_report(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    #  Verify interview ownership
    interview = db.query(Interview).filter(
        Interview.id == interview_id,
        Interview.user_id == current_user.id
    ).first()

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    if not interview.is_completed:
        raise HTTPException(
            status_code=400,
            detail="Interview not completed yet"
        )

    #  Fetch questions
    questions = db.query(Question).filter(
        Question.interview_id == interview.id
    ).all()

    report_questions = []
    all_answers_text = []

    for q in questions:
        answer = db.query(Answer).filter(
            Answer.question_id == q.id
        ).order_by(Answer.id.desc()).first()

        report_questions.append(
            ReportQuestion(
                id=q.id,
                question_text=q.content,
                user_answer=answer.user_answer if answer else None,
                score=answer.score if answer else None,
                feedback=answer.feedback if answer else None,
            )
        )

        if answer:
            all_answers_text.append(answer.user_answer)

    #  Average score calculation
    total_score = 0
    scored_count = 0

    for q in report_questions:
        if q.score is not None:
           total_score += q.score
           scored_count += 1

    avg_score = total_score / scored_count if scored_count else None


    #  AI Overall Evaluation

    overall_verdict = interview.overall_verdict

    return InterviewReportResponse(
        interview_id=interview.id,
        role=interview.role,
        difficulty=interview.difficulty,
        questions=report_questions,
        overall_verdict=overall_verdict,
        avg_score=avg_score,
        created_at=interview.created_at
    )



