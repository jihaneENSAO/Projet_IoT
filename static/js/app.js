// URL vers l’API Django
const API_URL = "/latest/";

// Sélecteurs pour les cartes (température & humidité)
const tempValue = document.getElementById("tempValue");
const humValue = document.getElementById("humValue");
const tempTime = document.getElementById("tempTime");
const humTime = document.getElementById("humTime");

// Sélecteurs pour les alertes / opérateurs
const incidentEl = document.getElementById("incident-status");
const alertCounterEl = document.getElementById("alert-counter");

const op1 = document.getElementById("op1");
const op2 = document.getElementById("op2");
const op3 = document.getElementById("op3");

let alertCount = 0;


// ----------------------------
//     LECTURE API BACKEND
// ----------------------------
async function loadLatest() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();

        const t = data.temperature;
        const h = data.humidity;
        const time = new Date(data.timestamp).toLocaleString();

        // Mise à jour des cartes
        tempValue.textContent = t + " °C";
        humValue.textContent = h + " %";

        tempTime.textContent = time;
        humTime.textContent = time;

        // ---------------------
        //   LOGIQUE INCIDENTS
        // ---------------------

        // Seuils : ici entre 2°C et 8°C (à changer si tu veux)
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
        //   OPÉRATEURS
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


// Lancement initial
loadLatest();

// Mise à jour toutes les 8 secondes
setInterval(loadLatest, 8000);
