document.addEventListener("DOMContentLoaded", () => {

    const tempCtx = document.getElementById('tempChart').getContext('2d');
    let tempChart;

        /* ===== EFFET FLOU / GLOW ===== */
    const originalLineDraw = Chart.controllers.line.prototype.draw;
    Chart.controllers.line.prototype.draw = function () {
        const ctx = this.chart.ctx;
        ctx.save();
        ctx.shadowColor = "rgba(255, 90, 31, 0.35)";
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

    async function loadTemp(animated = true) {

        const refreshBtn = document.getElementById("temp-refresh");
        refreshBtn.disabled = true;
        refreshBtn.textContent = "🔄 Chargement...";

        const date = document.getElementById("temp-date").value;
        const period = document.getElementById("temp-period").value;

        try {
            const res = await fetch(`/api/data/?date=${date}&period=${period}&_=${Date.now()}`);
            const data = await res.json();

            const labels = data.map(d => formatLabel(d.dt, period));
            const values = data.map(d => d.temp);

            if (!tempChart) {
                tempChart = new Chart(tempCtx, {
                    type: "line",
                    data: {
                        labels,
                        datasets: [{
                            label: "Température (°C)",
                            data: values,

                            /* 🔴 POINTS VISIBLES */
                            pointRadius: 4,
                            pointHoverRadius: 7,
                            pointBackgroundColor: "#ff5a1f",
                            pointBorderColor: "#ff5a1f",   
                            pointBorderWidth: 1,
                            /* effet flou */
                            pointHoverBorderWidth: 2,

                            /* LIGNE */
                            borderWidth: 3,
                            borderColor: "#ff5a1f",
                            backgroundColor: "rgba(255, 90, 31, 0.18)",
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
                                    color: "#9a3412",
                                    font: { weight: "bold" }
                                }
                            },
                            tooltip: {
                                backgroundColor: "#fff7ed",
                                titleColor: "#9a3412",
                                bodyColor: "#7c2d12",
                                borderColor: "#ff5a1f",
                                borderWidth: 1,
                                callbacks: {
                                    label: ctx => ` ${ctx.parsed.y} °C`
                                }
                            }
                        },
                        scales: {
                            x: {
                                grid: {
                                    color: "rgba(255, 180, 120, 0.25)"
                                },
                                ticks: {
                                    color: "#9a3412"
                                }
                            },
                            y: {
                                grid: {
                                    color: "rgba(255, 180, 120, 0.35)"
                                },
                                ticks: {
                                    color: "#9a3412"
                                },
                                title: {
                                    display: true,
                                    text: "Température (°C)",
                                    color: "#9a3412",
                                    font: { weight: "bold" }
                                }
                            }
                        }
                    }
                });
            } else {
                tempChart.data.labels = labels;
                tempChart.data.datasets[0].data = values;
                tempChart.update();
            }

        } catch (err) {
            console.error("Erreur chargement données température :", err);
            alert("Erreur lors du chargement des données !");
        } finally {
            refreshBtn.disabled = false;
            refreshBtn.textContent = "🔄 Actualiser";
        }
    }

    document.getElementById("temp-refresh").addEventListener("click", () => loadTemp(true));

    document.getElementById("temp-download").addEventListener("click", () => {
        const date = document.getElementById("temp-date").value;
        const period = document.getElementById("temp-period").value;
        window.location.href = `/api/export_csv_filtered/?date=${date}&period=${period}`;
    });

    loadTemp(false);
});
