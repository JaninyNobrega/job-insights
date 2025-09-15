from sqlmodel import SQLModel, create_engine, Session
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # pasta app/
DB_PATH = os.path.join(BASE_DIR, "..", "job_insights.db")

DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    from app.models import Job
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("✅ Banco e tabelas criados com sucesso!")
