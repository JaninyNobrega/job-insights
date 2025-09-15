import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from app.db import engine
from app.models import Job
from sqlmodel import Session
from datetime import datetime


def transform_remote_job(job: dict) -> Job:
    """
    Transforma a vaga recebida da API remota em um objeto Job do nosso banco.
    """
    return Job(
        title=job.get("title"),
        company=job.get("company"),
        location=job.get("location") or "Remoto",
        salary_min=job.get("salary_min"),
        salary_max=job.get("salary_max"),
        seniority=job.get("seniority") or "Não informado",
        posted_at=job.get("posted_at"),
        job_url=job.get("url"),   # 👈 novo campo para link da vaga
    )


def fetch_and_save_jobs():
    """
    Busca vagas reais de uma API pública e salva no banco de dados.
    Aqui usamos a Remotive API como exemplo.
    """
    print("🔎 Buscando vagas reais...")
    url = "https://remotive.com/api/remote-jobs"
    response = requests.get(url)

    if response.status_code != 200:
        print("❌ Erro ao buscar vagas:", response.text)
        return

    jobs_data = response.json().get("jobs", [])
    print(f"✅ {len(jobs_data)} vagas encontradas.")

    with Session(engine) as session:
        for job_data in jobs_data[:50]:  # pode ajustar para mais vagas
            job = transform_remote_job({
            "title": job_data.get("title"),
            "company": job_data.get("company_name"),
            "location": job_data.get("candidate_required_location"),
            "salary_min": None,
            "salary_max": None,
            "seniority": "Não informado",
            "posted_at": job_data.get("publication_date"),
            "url": job_data.get("url"),
        })
        session.add(job)
    session.commit()
    print("💾 Vagas salvas no banco com sucesso!")



if __name__ == "__main__":
    fetch_and_save_jobs()
