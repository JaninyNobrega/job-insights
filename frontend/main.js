const jobsContainer = document.getElementById("jobs-container");
const searchInput = document.getElementById("search");
const locationFilter = document.getElementById("filter-location");
const btnPDF = document.getElementById("btn-pdf");
const btnSearch = document.getElementById("btn-search"); // <-- novo

// FRONTEND: main.js
const BACKEND_BASE = "https://job-insights-st3y.onrender.com"; // <--- substitua aqui se mudar
const API_URL = `${BACKEND_BASE}/jobs/`;
const PDF_URL = `${BACKEND_BASE}/reports/pdf`;

let jobsData = [];

async function fetchJobs() {
    jobsContainer.innerHTML = "<p>Carregando vagas...</p>";
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Erro ao buscar vagas");

        jobsData = await response.json();
        // Ordena por data mais recente
        jobsData.sort((a, b) => new Date(b.posted_at) - new Date(a.posted_at));
        populateLocations();
        displayJobs();
    } catch (error) {
        jobsContainer.innerHTML = `<p>Erro ao carregar vagas. Verifique se o backend está rodando.</p>`;
        console.error(error);
    }
}

function populateLocations() {
    locationFilter.innerHTML = "";
    
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Todos os locais";
    locationFilter.appendChild(defaultOption);
    
    const locations = Array.from(new Set(jobsData.map(job => job.location))).sort();
    locations.forEach(loc => {
        const option = document.createElement("option");
        option.value = loc;
        option.textContent = loc;
        locationFilter.appendChild(option);
    });
}

function displayJobs() {
    const searchText = searchInput.value.toLowerCase();
    const selectedLocations = Array.from(locationFilter.selectedOptions).map(opt => opt.value);

    const filteredJobs = jobsData.filter(job => {
        const matchesSearch = job.title.toLowerCase().includes(searchText) ||
                              job.company.toLowerCase().includes(searchText);        
        const matchesLocation = selectedLocations.includes("") ? true : selectedLocations.includes(job.location);
        return matchesSearch && matchesLocation;
    });

    if (filteredJobs.length === 0) {
        jobsContainer.innerHTML = "<p>Nenhuma vaga encontrada.</p>";
        return;
    }

    jobsContainer.innerHTML = filteredJobs.map(job => `
        <div class="job-card">
            <h3>${job.title}</h3>
            <p><strong>Empresa:</strong> ${job.company}</p>
            <p><strong>Local:</strong> ${job.location}</p>
            <p><strong>Salário:</strong> ${job.salary_min ?? 'Não informado'} - ${job.salary_max ?? 'Não informado'}</p>
            <p><strong>Senioridade:</strong> ${job.seniority}</p>
            ${job.job_url ? `<p><a href="${job.job_url}" target="_blank">Ver vaga</a></p>` : ""}
        </div>
    `).join('');
}

function generatePDF() {
    window.open(PDF_URL, "_blank");
}

// Eventos
searchInput.addEventListener("input", displayJobs);
locationFilter.addEventListener("change", displayJobs);
btnPDF.addEventListener("click", generatePDF);
btnSearch.addEventListener("click", displayJobs); // <-- novo evento

// Inicializa
fetchJobs();
