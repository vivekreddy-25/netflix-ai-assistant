from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.pipeline import run_pipeline
import pandas as pd
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

    if isinstance(result, pd.DataFrame):
        if result.empty:
            answer = "No matching movies found."
        else:
            lines = [
                f"{row['title']} ({int(row['release_year'])}) | {row['genres']}"
                for _, row in result.iterrows()
            ]
            answer = "\n".join(lines)
    else:
        answer = str(result)

    return AnswerResponse(answer=answer)