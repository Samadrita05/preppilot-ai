from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


# ---------- AUTH SCHEMAS ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# ---------- INTERVIEW SCHEMAS ----------

class InterviewCreate(BaseModel):
    role: str
    difficulty: str

class InterviewResponse(BaseModel):
    id: int
    role: str
    difficulty: str
    is_completed: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionResponse(BaseModel):
    id: int
    question_text: str

class QuestionGenerateResponse(BaseModel):
    interview_id: int
    questions: List[QuestionResponse]

# ---------- ANSWER SCHEMAS ----------

class AnswerCreate(BaseModel):
    user_answer: str

class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_answer: str
    score: Optional[float]
    feedback: Optional[str]

    class Config:
        from_attributes = True

# ---------- REPORT SCHEMAS ----------

class ReportQuestion(BaseModel):
    id: int
    question_text: str
    user_answer: Optional[str]
    score: Optional[float]
    feedback: Optional[str]

class InterviewReportResponse(BaseModel):
    interview_id: int
    role: str
    difficulty: str
    questions: List[ReportQuestion]
    overall_verdict: Optional[str] = None
    avg_score: Optional[float]
    created_at: Optional[datetime]