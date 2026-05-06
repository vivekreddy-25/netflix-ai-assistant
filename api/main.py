from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.pipeline import run_pipeline

app = FastAPI(title="Netflix AI API")


# Request model
class QuestionRequest(BaseModel):
    question: str


# Response model
class AnswerResponse(BaseModel):
    answer: str


# Root route
@app.get("/")
def root():
    return {"status": "ok", "message": "Netflix AI API running"}


# Main AI endpoint
@app.post("/ask", response_model=AnswerResponse)
def ask_question(body: QuestionRequest):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    result = run_pipeline(body.question)

    return AnswerResponse(answer=str(result))