# backend/routers/interview.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import InterviewQuestion, InterviewAnswer
from ..schemas import (
    QuestionRequest, QuestionResponse,
    AnswerCreateRequest, AnswerCreateOut,
    AnswerEvaluationRequest, AnswerEvaluation
)
from ..services import generate_interview_questions, evaluate_interview_answer

router = APIRouter(prefix="/interviews", tags=["interviews"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/questions", response_model=QuestionResponse)
async def generate_questions(req: QuestionRequest):
    """GPT 호출로 질문 생성"""
    try:
        questions = generate_interview_questions(req.user_id, req.company, req.role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"질문 생성 실패: {e}")
    return {"questions": questions}


@router.post("/answers", response_model=AnswerCreateOut)
async def create_answer(info: AnswerCreateRequest, db: Session = Depends(get_db)):
    print("🔔 create_answer hit! payload:", info)
    """DB에 답변 저장 후, answer.id 리턴"""
    # 1) 질문 존재 확인
    question = db.query(InterviewQuestion).filter_by(id=info.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # 2) 답변 저장
    ans = InterviewAnswer(
        question_id=info.question_id,
        answer_text=info.answer_text,
        score=None,
        feedback=None
    )
    db.add(ans)
    db.commit()
    db.refresh(ans)

    # 3) 생성된 answer ID 리턴
    return {"id": ans.id}


@router.post("/evaluate/{answer_id}", response_model=AnswerEvaluation)
async def evaluate_answer(answer_id: int, req: AnswerEvaluationRequest, db: Session = Depends(get_db)):
    """DB에서 답변 불러와 GPT 평가, 점수·피드백 저장 후 리턴"""
    # 1) 저장된 답변 가져오기
    answer = db.query(InterviewAnswer).filter_by(id=answer_id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    # 2) GPT 평가
    try:
        result = evaluate_interview_answer(answer.answer_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"평가 실패: {e}")

    # 3) DB에 결과 기록
    answer.score = result["score"]
    answer.feedback = result["feedback"]
    db.commit()

    # 4) 클라이언트에 결과 반환
    return {"score": answer.score, "feedback": answer.feedback}