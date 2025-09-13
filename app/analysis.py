from sqlmodel import Session, select
from app.models import Job
from app.db import get_session
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def get_jobs_df(session: Session):
    """Transforma as vagas do banco em DataFrame pandas"""
    jobs = session.exec(select(Job)).all()
    df = pd.DataFrame([{
        "title": j.title,
        "company": j.company,
        "location": j.location,
        "salary_min": j.salary_min,
        "salary_max": j.salary_max,
        "seniority": j.seniority,
        "posted_at": j.posted_at
    } for j in jobs])
    return df

def salary_analysis(session: Session):
    """Gera estatísticas salariais e gráfico"""
    df = get_jobs_df(session)
    if df.empty:
        return {"message": "Sem dados para análise"}
    
    # Média salarial por senioridade
    df['salary_avg'] = df[['salary_min', 'salary_max']].mean(axis=1)
    salary_by_seniority = df.groupby('seniority')['salary_avg'].mean().to_dict()
    
    # Gráfico de barras
    plt.figure(figsize=(6,4))
    df.groupby('seniority')['salary_avg'].mean().plot(kind='bar')
    plt.title("Salário médio por senioridade")
    plt.ylabel("R$")

    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    # Converte para base64 para enviar via API
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return {
        "salary_by_seniority": salary_by_seniority,
        "chart_base64": img_base64
    }

def jobs_by_location(session: Session):
    """Conta quantidade de vagas por cidade"""
    df = get_jobs_df(session)
    if df.empty:
        return {"message": "Sem dados para análise"}
    
    count_location = df['location'].value_counts().to_dict()
    return count_location
