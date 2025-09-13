import pandas as pd
from sqlmodel import Session
from app.db import engine
from app.models import Job

# Lê o CSV
df = pd.read_csv("data/jobs.csv")

with Session(engine) as session:
    for _, row in df.iterrows():
        job = Job(
            title=row['title'],
            company=row['company'],
            location=row['location'],
            salary_min=row['salary_min'],
            salary_max=row['salary_max'],
            seniority=row['seniority'],
            posted_at=row['posted_at']
        )
        session.add(job)
    session.commit()

print("Banco populado com sucesso!")
