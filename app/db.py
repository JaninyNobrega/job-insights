import os
from sqlmodel import create_engine, Session, SQLModel

# Usa SQLite local por padrão (mais simples para iniciar)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_insights.db")
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
