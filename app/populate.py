import requests
from datetime import datetime
from app.models import Job

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"

def populate_jobs(session):
    print("🔄 Buscando vagas da Remotive...")
    try:
        response = requests.get(REMOTIVE_API_URL)
        response.raise_for_status()
        data = response.json()

        jobs_data = data.get("jobs", [])[:10]  # pega só as 10 primeiras vagas

        job_entries = []
        for job in jobs_data:
            job_entries.append(
                Job(
                    title=job.get("title", "Sem título"),
                    company=job.get("company_name", "Desconhecida"),
                    location=job.get("candidate_required_location", "Remoto"),
                    salary_min=None,  # Remotive não fornece salário fixo
                    salary_max=None,
                    seniority=job.get("job_type", "N/A"),
                    posted_at=datetime.fromisoformat(job["publication_date"].replace("Z", "+00:00")),
                    job_url=job.get("url", "#")
                )
            )

        if job_entries:
            session.add_all(job_entries)
            session.commit()
            print(f"✅ {len(job_entries)} vagas adicionadas ao banco.")
        else:
            print("⚠️ Nenhuma vaga encontrada na API.")

    except Exception as e:
        print("❌ Erro ao buscar vagas da Remotive:", e)
