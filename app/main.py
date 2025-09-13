from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.db import get_session, create_db_and_tables
from app.models import Job
from typing import List

app = FastAPI(title="Job Insights API")

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
