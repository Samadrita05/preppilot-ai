from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite frontend
        "http://127.0.0.1:5173",
        "https://preppilot-ai-s8u2.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],   # THIS ENABLES OPTIONS
    allow_headers=["*"],
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

