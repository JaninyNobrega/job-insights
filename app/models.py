from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    seniority: Optional[str] = None
    posted_at: Optional[date] = None
