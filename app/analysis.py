from sqlmodel import Session, select
from app.models import Job
from collections import defaultdict

def salary_analysis(session: Session) -> dict:
    """Retorna média salarial por senioridade e gráfico"""
    stmt = select(Job)
    jobs = session.exec(stmt).all()

    salary_by_seniority = defaultdict(list)
    for job in jobs:
        avg_salary = (job.salary_min + job.salary_max) / 2
        salary_by_seniority[job.seniority].append(avg_salary)

    result = {}
    for seniority, salaries in salary_by_seniority.items():
        result[seniority] = sum(salaries)/len(salaries)

    return {"salary_by_seniority": result}

def jobs_by_location(session: Session) -> dict:
    stmt = select(Job)
    jobs = session.exec(stmt).all()

    counts = defaultdict(int)
    for job in jobs:
        counts[job.location] += 1

    return dict(counts)
