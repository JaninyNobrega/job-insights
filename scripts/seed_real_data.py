import pandas as pd
from app.db import engine
from sqlmodel import Session
from app.models import Job

def seed_data():
    df = pd.read_csv("data/jobs.csv")

    with Session(engine) as session:
        for _, row in df.iterrows():
            job = Job(
                title=row["title"],
                company=row["company"],
                location=row["location"],
                salary_min=row["salary_min"],
                salary_max=row["salary_max"],
                seniority=row["seniority"],
                posted_at=row["posted_at"]
            )
            session.add(job)
        session.commit()
    print("✅ Dados populados com sucesso!")

if __name__ == "__main__":
    seed_data()
