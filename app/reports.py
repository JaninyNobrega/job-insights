import matplotlib
matplotlib.use("Agg")
from sqlmodel import Session
from app.analysis import salary_analysis, jobs_by_location
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os

def generate_pdf_report(session: Session) -> bytes:
    """Gera PDF com análises de salários e vagas por cidade"""
    try:
        analysis = salary_analysis(session)
        salary_by_seniority = analysis.get("salary_by_seniority", {})
        print("Dados salary_by_seniority:", salary_by_seniority)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório Job Insights", ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.ln(5)
        pdf.cell(0, 10, "Média Salarial por Senioridade:", ln=True)
        pdf.ln(2)

        for seniority, avg_salary in salary_by_seniority.items():
            pdf.cell(0, 10, f"{seniority}: R$ {avg_salary:.2f}", ln=True)

        # Bloco do gráfico salarial
        if salary_by_seniority:
            try:
                plt.figure(figsize=(6, 4))
                plt.bar(salary_by_seniority.keys(), salary_by_seniority.values(), color="skyblue")
                plt.title("Média Salarial por Senioridade")
                plt.xlabel("Senioridade")
                plt.ylabel("Salário Médio")
                plt.tight_layout()

                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                    plt.savefig(tmpfile.name)
                    pdf.ln(5)
                    pdf.image(tmpfile.name, x=10, y=pdf.get_y()+5, w=180)
                    tmp_path = tmpfile.name

                plt.close()
                os.remove(tmp_path)
            except Exception as e:
                print("Erro ao gerar o gráfico:", e)
                plt.close()

        # Vagas por cidade
        location_counts = jobs_by_location(session)
        print("Dados jobs_by_location:", location_counts)

        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Vagas por Cidade:", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", "", 12)
        for location, count in location_counts.items():
            pdf.cell(0, 10, f"{location}: {count} vagas", ln=True)

        return pdf.output(dest="S")
    except Exception as exc:
        print("Erro na geração do PDF:", exc)
        raise
