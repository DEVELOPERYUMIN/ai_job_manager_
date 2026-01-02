# schemas.py

from pydantic import BaseModel
from typing import List

# ▶ Resume 쪽 스키마
class ResumeCreate(BaseModel):
    user_id: int
    text: str

class ResumeOut(BaseModel):
    id: int
    user_id: int
    original_text: str

    class Config:
        orm_mode = True

class ResumeFeedbackRequest(BaseModel):
    pass

class ResumeFeedbackOut(BaseModel):
    edited_text: str
    feedback: str

    class Config:
        orm_mode = True

# ▶ Resume 새 생성 기능 스키마
class ResumeGenerateRequest(BaseModel):
    name: str
    role: str
    experience_years: int
    experience_list: str

class ResumeGenerateOut(BaseModel):
    generated_text: str

    class Config:
        orm_mode = True


# ▶ Interview 쪽 스키마
class QuestionRequest(BaseModel):
    user_id: int
    company: str
    role: str

class QuestionResponse(BaseModel):
    questions: List[str]

class AnswerCreateRequest(BaseModel):
    question_id: int
    answer_text: str

class AnswerCreateOut(BaseModel):
    id: int
    question_id: int
    answer_text: str

    class Config:
        orm_mode = True

class AnswerEvaluationRequest(BaseModel):
    # 핸들러가 request.answer를 사용하지 않는다면 빈 JSON만 받도록 pass 처리
    pass

class AnswerEvaluation(BaseModel):
    score: float
    feedback: str


# ▶ Dashboard 쪽 스키마
class DashboardOut(BaseModel):
    user_id: int
    user_name: str
    total_resumes: int
    reviewed_resumes: int
    total_questions: int
    total_answers: int
    total_evaluated_answers: int

    class Config:
        orm_mode = True


# ▶ Export 쪽 스키마
class ExportResponse(BaseModel):
    filename: str
    download_url: str

    class Config:
        orm_mode = True

