from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.db import get_session, create_db_and_tables
from app.models import Job
from typing import List
from app.analysis import salary_analysis, jobs_by_location
from fastapi.responses import StreamingResponse
from app.reports import generate_pdf_report
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Job Insights API")

origins = [
    "http://127.0.0.1:5500",  # endereço do frontend
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Job Insights API rodando 🚀"}

@app.post("/jobs/", response_model=Job)
def create_job(job: Job, session: Session = Depends(get_session)):
    session.add(job)
    session.commit()
    session.refresh(job)
    return job

@app.get("/jobs/", response_model=List[Job])
def list_jobs(session: Session = Depends(get_session)):
    return session.exec(select(Job)).all()

@app.get("/analytics/salary")
def analytics_salary(session: Session = Depends(get_session)):
    result = salary_analysis(session)
    if "salary_by_seniority" not in result:
        result = {"salary_by_seniority": {}, "chart_base64": None}
    return result

@app.get("/analytics/location")
def analytics_location(session: Session = Depends(get_session)):
    return jobs_by_location(session)

@app.get("/reports/pdf")
def reports_pdf(session: Session = Depends(get_session)):
    pdf_bytes = generate_pdf_report(session)
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=job_insights.pdf"}
    )
