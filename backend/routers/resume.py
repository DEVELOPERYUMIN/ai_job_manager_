from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from ..models import Resume, User
from ..schemas import (
    ResumeCreate, ResumeOut,
    ResumeFeedbackRequest, ResumeFeedbackOut,
    ResumeGenerateRequest, ResumeGenerateOut
)
from ..services import give_resume_feedback, gpt_client

# prefix를 라우터에만 지정하여 중복 제거
router = APIRouter(prefix="/resumes", tags=["resumes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ▶ 업로드된 자기소개서 전체 목록 조회
@router.get("", response_model=List[ResumeOut])
def list_resumes(db: Session = Depends(get_db)):
    """
    React 쪽 getResumeList() 호출용 GET 엔드포인트
    """
    return db.query(Resume).all()

# ▶ 자기소개서 업로드
@router.post("", response_model=ResumeOut)
def upload_resume(
    payload: ResumeCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == payload.user_id).first()
    if user is None:
        user = User(id=payload.user_id, name=f"User{payload.user_id}")
        db.add(user)
        db.commit()
        db.refresh(user)

    resume = Resume(user_id=payload.user_id, original_text=payload.text)
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume

# ▶ 자기소개서 첨삭 요청
@router.post("/{resume_id}/feedback", response_model=ResumeFeedbackOut)
def give_feedback(
    resume_id: int,
    _: ResumeFeedbackRequest,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    result = give_resume_feedback(resume.original_text)
    resume.edited_text = result["edited_text"]
    resume.feedback = result["feedback"]
    db.commit()
    db.refresh(resume)

    return ResumeFeedbackOut(
        edited_text=resume.edited_text,
        feedback=resume.feedback
    )

# ▶ 새 자기소개서 생성
@router.post("/generate", response_model=ResumeGenerateOut)
def generate_resume(
    r: ResumeGenerateRequest
):
    system_prompt = (
        "당신은 커리어 코치입니다. 지원자의 정보를 바탕으로 매력적인 자기소개서를 작성해 주세요."
    )
    user_prompt = (
        f"이름: {r.name}\n"
        f"희망직무: {r.role}\n"
        f"경력(년): {r.experience_years}\n"
        f"경험 요약: {r.experience_list}\n"
        "위 정보를 바탕으로 400자 분량의 자기소개서를 작성해 주세요."
    )
    generated_text = gpt_client.chat(system_prompt, user_prompt)
    return {"generated_text": generated_text}
