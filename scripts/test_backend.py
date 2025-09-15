import sys
import os

# Garante que a pasta app seja encontrada
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import create_db_and_tables, get_session, engine
from app.models import Job
from sqlmodel import Session
import requests
from datetime import datetime

def transform_remote_job(job_data):
    posted_at_str = job_data.get("publication_date")

    # Converte a string ISO em datetime, se existir
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
        posted_at=posted_at,  # agora é datetime
        job_url=job_data.get("url"),
    )


def fetch_and_save_jobs(limit=10):
    print("🔎 Buscando vagas reais...")
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Erro ao buscar vagas:", response.text)
        return

    jobs_data = response.json().get("jobs", [])
    print(f"✅ {len(jobs_data)} vagas encontradas.")

    # Salva no banco
    with Session(engine) as session:
        for job_data in jobs_data[:limit]:
            job = transform_remote_job(job_data)
            session.add(job)
        session.commit()
    print("💾 Vagas salvas no banco com sucesso!")

def list_jobs():
    print("📄 Listando vagas salvas no banco...")
    with Session(engine) as session:
        jobs = session.query(Job).all()
        print(f"Total de vagas: {len(jobs)}")
        for job in jobs:
            print(f"{job.title} | {job.company} | {job.location} | {job.job_url}")

if __name__ == "__main__":
    # Cria o banco e as tabelas
    create_db_and_tables()
    # Busca e salva vagas reais
    fetch_and_save_jobs()
    # Lista as vagas salvas
    list_jobs()
