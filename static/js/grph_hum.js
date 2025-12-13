async function loadHumHistory() {
    const res = await fetch("/api/");
    const json = await res.json();

    if (!json.data || json.data.length === 0) return;

    const labels = json.data.map(row =>
        new Date(row.dt_iso).toLocaleTimeString("fr-FR")
    );
    const hums = json.data.map(row => row.hum);

    new Chart(document.getElementById("humChart"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Humidité (%)",
                data: hums,
                borderColor: "blue",
                backgroundColor: "rgba(51,153,255,0.2)",
                borderWidth: 2,
                tension: 0.4,
                fill: true,
                pointRadius: 3,
                pointBackgroundColor: "#0066cc"
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                x: { grid: { color: "#cce6ff" } },
                y: { grid: { color: "#cce6ff" } }
            }
        }
    });
}

loadHumHistory();
