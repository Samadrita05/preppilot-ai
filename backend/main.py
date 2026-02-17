from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base
from database import models

app = FastAPI()
Base.metadata.create_all(bind=engine)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://preppilot-ai-s8u2.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

from routers import auth, interview, question, answer, report

app.include_router(auth.router)
app.include_router(interview.router)
app.include_router(question.router)
app.include_router(answer.router)
app.include_router(report.router)
@app.get("/")
def home():
    return {"message": "PrepPilot Backend is running successfully 🚀"}

