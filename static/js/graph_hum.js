document.addEventListener("DOMContentLoaded", () => {

    const humCtx = document.getElementById('humChart').getContext('2d');
    let humChart;

    /* ===== EFFET FLOU / GLOW ===== */
    const originalLineDraw = Chart.controllers.line.prototype.draw;
    Chart.controllers.line.prototype.draw = function () {
        const ctx = this.chart.ctx;
        ctx.save();
        ctx.shadowColor = "rgba(30, 64, 175, 0.35)";
        ctx.shadowBlur = 8;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;
        originalLineDraw.apply(this, arguments);
        ctx.restore();
    };

    function formatLabel(dt, period) {
        const d = new Date(dt.replace(" ", "T"));
        if (period === "day") {
            return d.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
        }
        return d.toLocaleDateString("fr-FR") + " " +
            d.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
    }

    async function loadHum(animated = true) {
        const refreshBtn = document.getElementById("hum-refresh");
        refreshBtn.disabled = true;
        refreshBtn.textContent = "🔄 Chargement...";

        const date = document.getElementById("hum-date").value;
        const period = document.getElementById("hum-period").value;

        try {
            const res = await fetch(`/api/data/?date=${date}&period=${period}&_=${Date.now()}`);
            const data = await res.json();

            const labels = data.map(d => formatLabel(d.dt, period));
            const values = data.map(d => d.hum);

            if (!humChart) {
                humChart = new Chart(humCtx, {
                    type: "line",
                    data: {
                        labels,
                        datasets: [{
                            label: "Humidité (%)",
                            data: values,
                            pointRadius: 4,
                            pointHoverRadius: 7,
                            pointBackgroundColor: "#1e40af",
                            pointBorderColor: "#1e40af",
                            pointBorderWidth: 1,
                            pointHoverBorderWidth: 2,
                            borderWidth: 3,
                            borderColor: "#1e40af",
                            backgroundColor: "rgba(30, 64, 175, 0.18)",
                            tension: 0.45,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        animation: animated,
                        interaction: {
                            mode: "index",
                            intersect: false
                        },
                        plugins: {
                            legend: {
                                labels: {
                                    color: "#1e3a8a",
                                    font: { weight: "bold" }
                                }
                            },
                            tooltip: {
                                backgroundColor: "#ebf4ff",
                                titleColor: "#1e3a8a",
                                bodyColor: "#1e40af",
                                borderColor: "#1e40af",
                                borderWidth: 1,
                                callbacks: {
                                    label: ctx => ` ${ctx.parsed.y} %`
                                }
                            }
                        },
                        scales: {
                            x: {
                                grid: { color: "rgba(100, 149, 237, 0.25)" },
                                ticks: { color: "#1e3a8a" }
                            },
                            y: {
                                grid: { color: "rgba(100, 149, 237, 0.35)" },
                                ticks: { color: "#1e3a8a" },
                                title: {
                                    display: true,
                                    text: "Humidité (%)",
                                    color: "#1e3a8a",
                                    font: { weight: "bold" }
                                }
                            }
                        }
                    }
                });
            } else {
                humChart.data.labels = labels;
                humChart.data.datasets[0].data = values;
                humChart.update();
            }

        } catch (err) {
            console.error("Erreur chargement données humidité :", err);
            alert("Erreur lors du chargement des données !");
        } finally {
            refreshBtn.disabled = false;
            refreshBtn.textContent = "🔄 Actualiser";
        }
    }

    document.getElementById("hum-refresh").addEventListener("click", () => loadHum(true));

    document.getElementById("hum-download").addEventListener("click", () => {
        const date = document.getElementById("hum-date").value;
        const period = document.getElementById("hum-period").value;
        window.location.href = `/api/export_csv_filtered/?date=${date}&period=${period}`;
    });

    loadHum(false);
});
