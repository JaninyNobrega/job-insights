from app.db import get_session
from app.models import Job

session = next(get_session())
jobs = session.query(Job).all()
for job in jobs:
    print(job.title, job.salary_min, job.salary_max, job.seniority, job.location)
