const API_URL = "/latest/";

// Sélecteurs pour les cartes
const tempValue = document.getElementById("tempValue");
const humValue = document.getElementById("humValue");
const tempTime = document.getElementById("tempTime");
const humTime = document.getElementById("humTime");

// Sélecteurs pour alertes / opérateurs
const incidentEl = document.getElementById("incident-status");
const alertCounterEl = document.getElementById("alert-counter");
const op1 = document.getElementById("op1");
const op2 = document.getElementById("op2");
const op3 = document.getElementById("op3");

let alertCount = 0;

async function loadLatest() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        const t = data.temp;       // clé conforme à ton endpoint /latest/
        const h = data.hum;
        const time = new Date(data.dt_iso).toLocaleString();

        // Mise à jour cartes
        tempValue.textContent = t + " °C";
        humValue.textContent = h + " %";
        tempTime.textContent = time;
        humTime.textContent = time;

        // ---------------------
        // Logique incidents
        // ---------------------
        if (t < 2 || t > 8) {
            incidentEl.textContent = "⚠️ Incident : température hors plage !";
            incidentEl.style.color = "red";
            alertCount++;
        } else {
            incidentEl.textContent = "Aucun incident";
            incidentEl.style.color = "green";
            alertCount = 0;
        }

        alertCounterEl.textContent = "Compteur alertes : " + alertCount;

        // ---------------------
        // Opérateurs
        // ---------------------
        op1.style.display = alertCount > 0 ? "block" : "none";
        op2.style.display = alertCount > 3 ? "block" : "none";
        op3.style.display = alertCount > 6 ? "block" : "none";

    } catch (err) {
        console.error("Erreur API:", err);
        incidentEl.textContent = "Erreur de connexion au serveur";
        incidentEl.style.color = "darkred";
    }
}

// Lancement initial + mise à jour toutes les 8 secondes
loadLatest();
setInterval(loadLatest, 8000);
