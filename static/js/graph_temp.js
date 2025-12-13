async function loadTempHistory() {
    const res = await fetch("/api/");
    const json = await res.json();

    if (!json.data || json.data.length === 0) return;

    const labels = json.data.map(row =>
        new Date(row.dt_iso).toLocaleTimeString("fr-FR")
    );
    const temps = json.data.map(row => row.temp);

    new Chart(document.getElementById("tempChart"), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Température (°C)",
                data: temps,
                borderColor: "#ff6b35",
                backgroundColor: "rgba(255,107,53,0.2)",
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointRadius: 4,
                pointBackgroundColor: "#ff3d00"
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' }
            },
            scales: {
                x: {
                    ticks: { color: "#bf360c" },
                    grid: { color: "#ffe6dc" }
                },
                y: {
                    ticks: { color: "#bf360c" },
                    grid: { color: "#ffe6dc" }
                }
            }
        }
    });
}

loadTempHistory();
