
from fastapi import FastAPI
from .database import Base, engine
from .routers import resume, interview, dashboard, exporter
from fastapi.middleware.cors import CORSMiddleware

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Prep Assistant")
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],    # 필요하다면 프런트엔드 주소만 명시해도 됩니다.
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
app.include_router(resume.router, tags=["Resumes"])
app.include_router(interview.router,tags=["Interviews"])
app.include_router(dashboard.router,tags=["Dashboard"])
app.include_router(exporter.router, prefix="/exporter", tags=["Exporter"])
