from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from app.db import get_session, create_db_and_tables, engine
from app.models import Job
from app.analysis import salary_analysis, jobs_by_location
from fastapi.responses import StreamingResponse
from app.reports import generate_pdf_report
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
from typing import List
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Job Insights API")

# Configuração CORS para frontend
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

# Sirva o diretório frontend (certifique-se de que o caminho esteja correto)
# app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# Função para transformar dados da API externa em Job
def transform_remote_job(job_data):
    posted_at_str = job_data.get("publication_date")
    posted_at = None
    if posted_at_str:
        try:
            posted_at = datetime.fromisoformat(posted_at_str.replace("Z", "+00:00"))
        except ValueError:
            posted_at = None
    return Job(
        title=job_data.get("title"),
        company=job_data.get("company_name"),
        location=job_data.get("candidate_required_location") or "Remoto",
        salary_min=None,
        salary_max=None,
        seniority="Não informado",
        posted_at=posted_at,
        job_url=job_data.get("url"),
    )

# Função para buscar e salvar vagas externas
def fetch_and_save_jobs(limit=20):
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Erro ao buscar vagas:", response.text)
        return
    jobs_data = response.json().get("jobs", [])
    with Session(engine) as session:
        for job_data in jobs_data[:limit]:
            job = transform_remote_job(job_data)
            session.add(job)
        session.commit()
    print(f"💾 {len(jobs_data[:limit])} vagas salvas no banco.")

# Evento de startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # Popular o banco automaticamente se estiver vazio
    with Session(engine) as session:
        total_jobs = session.exec(select(Job)).count()
        if total_jobs == 0:
            print("Banco vazio. Populando com vagas iniciais...")
            fetch_and_save_jobs()
        else:
            print(f"Banco já possui {total_jobs} vagas.")

# Endpoints
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
