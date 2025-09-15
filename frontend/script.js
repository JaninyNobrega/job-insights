const jobsContainer = document.getElementById('jobs-container');
const searchInput = document.getElementById('search');

// Função para buscar vagas
async function fetchJobs() {
  try {
    const response = await fetch('http://127.0.0.1:9000/jobs/');
    const jobs = await response.json();
    displayJobs(jobs);
  } catch (error) {
    jobsContainer.innerHTML = `<p>Erro ao carregar vagas. Verifique se o backend está rodando.</p>`;
    console.error(error);
  }
}

// Função para mostrar as vagas
function displayJobs(jobs) {
  jobsContainer.innerHTML = '';
  const filterText = searchInput.value.toLowerCase();

  const filteredJobs = jobs.filter(job => 
    job.title.toLowerCase().includes(filterText) || 
    job.company.toLowerCase().includes(filterText)
  );

  if (filteredJobs.length === 0) {
    jobsContainer.innerHTML = '<p>Nenhuma vaga encontrada.</p>';
    return;
  }

  filteredJobs.forEach(job => {
    const card = document.createElement('div');
    card.classList.add('job-card');
    card.innerHTML = `
      <h3>${job.title}</h3>
      <p><strong>Empresa:</strong> ${job.company}</p>
      <p><strong>Local:</strong> ${job.location}</p>
      <p><strong>Salário:</strong> ${job.salary_min ?? 'N/A'} - ${job.salary_max ?? 'N/A'}</p>
      <p><strong>Senioridade:</strong> ${job.seniority}</p>
      <p><strong>Postado em:</strong> ${new Date(job.posted_at).toLocaleDateString()}</p>
      <p><a href="${job.job_url}" target="_blank">Ver vaga</a></p>
    `;
    jobsContainer.appendChild(card);
  });
}

// Eventos
searchInput.addEventListener('input', fetchJobs);

// Inicializa
fetchJobs();
