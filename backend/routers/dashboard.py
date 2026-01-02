
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User, Resume, InterviewQuestion, InterviewAnswer
from ..schemas import DashboardOut

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_model=DashboardOut)
def get_dashboard(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_resumes = db.query(Resume).filter(Resume.user_id == user_id).count()
    reviewed_resumes = db.query(Resume).filter(
        Resume.user_id == user_id, Resume.edited_text.isnot(None)
    ).count()
    total_questions = db.query(InterviewQuestion).filter(InterviewQuestion.user_id == user_id).count()
    total_answers = db.query(InterviewAnswer).join(
        InterviewQuestion, InterviewQuestion.id == InterviewAnswer.question_id
    ).filter(InterviewQuestion.user_id == user_id).count()
    total_evaluated_answers = db.query(InterviewAnswer).join(
        InterviewQuestion, InterviewQuestion.id == InterviewAnswer.question_id
    ).filter(
        InterviewQuestion.user_id == user_id, InterviewAnswer.score.isnot(None)
    ).count()

    return {
        "user_id": user_id,
        "user_name": user.name,
        "total_resumes": total_resumes,
        "reviewed_resumes": reviewed_resumes,
        "total_questions": total_questions,
        "total_answers": total_answers,
        "total_evaluated_answers": total_evaluated_answers
    }
