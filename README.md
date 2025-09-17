# Job Insights API 🚀💼

![Status](https://img.shields.io/badge/Status-Em%20funcionamento-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-cyan)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

**Job Insights API** é uma aplicação backend moderna construída com **Python e FastAPI** que coleta, armazena e analisa vagas de trabalho remoto automaticamente.  


---

## 🎬 Demonstração (GIF ou screenshots)

![Dashboard GIF](https://media.giphy.com/media/3o7TKtnuHOHHUjR38Y/giphy.gif)  
*Exemplo de geração de relatórios em PDF e análise de dados de vagas*

![Mapa de vagas](https://via.placeholder.com/600x300.png?text=Mapa+de+vagas+por+país)  
*Distribuição das vagas por país / localização*

---

## 🛠 Tecnologias utilizadas

- **Python 3.11+** – Linguagem principal  
- **FastAPI** – Framework rápido e moderno  
- **SQLModel / SQLAlchemy** – ORM para modelagem de dados  
- **PostgreSQL** – Banco de dados relacional  
- **APScheduler** – Tarefas agendadas automaticamente  
- **Requests** – Consumo de API externa (Remotive)  
- **Faker** – Popula dados iniciais  
- **PDF Reports** – Relatórios prontos para download  
- **CORS Middleware** – Suporte a frontends externos  

---

## 🔍 Funcionalidades principais

- Coleta automática de vagas remotas da **Remotive API**  
- Atualização programada a cada 6 horas (configurável)  
- População inicial do banco caso esteja vazio  
- Endpoints de consulta e criação de vagas:
  - `GET /jobs/` – Lista todas as vagas  
  - `POST /jobs/` – Cria nova vaga  
  - `GET /analytics/salary` – Salários por senioridade  
  - `GET /analytics/location` – Vagas por localização  
  - `GET /reports/pdf` – Relatório em PDF completo  
- Suporte a frontends externos com CORS configurado  

---

## 📈 Insights & Análises

- **Salário médio por senioridade**  
- **Distribuição de vagas por país/cidade**  
- **Relatórios em PDF** prontos para download  
- **Visualizações prontas para dashboards ou apresentações**  

---

## 💻 Estrutura do projeto


---

## 🚀 Como rodar localmente

1. Clone o repositório:

```bash
git clone https://github.com/JaninyNobrega/job-insights.git
cd job-insights

2. Crie um ambiente virtual:

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows


3. Instale as dependências:

pip install -r requirements.txt


4. Inicialize o banco de dados:

from app.db import create_db_and_tables
create_db_and_tables()


5. Rode a aplicação:

uvicorn app.main:app --reload


A API estará disponível em: http://127.0.0.1:8000


🌟 Diferenciais

Código limpo, modular e escalável, pronto para produção

Atualizações automáticas de vagas com APScheduler

Insights reais do mercado remoto para tomada de decisão

Geração de relatórios em PDF completos e profissionais

📝 Próximos passos / melhorias

Integração com APIs adicionais (LinkedIn, Indeed, etc.)

Dashboard frontend interativo com gráficos dinâmicos

Filtragem avançada de vagas por tecnologia, senioridade ou salário

🔗 Links

Documentação da API (Swagger)

Documentação da API (Redoc)

Netlify / Frontend https://job-insights-vagas.netlify.app/
Render / Backend https://job-insights-st3y.onrender.com/

🏷 Licença

MIT License