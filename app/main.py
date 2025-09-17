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
from app.populate import populate_jobs
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = FastAPI()

# Configuração CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_origin_regex=r"https://.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # Cria as tabelas antes de usar
    create_db_and_tables()

    with Session(engine) as session:
        total_jobs = len(session.exec(select(Job)).all())
        if total_jobs == 0:
            print("💡 Nenhuma vaga encontrada. Populando banco de dados...")
            populate_jobs(session)
            print("✅ Banco populado com sucesso!")
        else:
            print(f"🔎 Banco já possui {total_jobs} vagas.")

# --- Agendador para atualizar as vagas automaticamente ---
scheduler = BackgroundScheduler()

def job_update():
    print("🔄 Atualizando vagas automaticamente...")
    with Session(engine) as session:
        populate_jobs(session)

# Configura para rodar a cada 6 horas
scheduler.add_job(job_update, IntervalTrigger(hours=6))
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

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
