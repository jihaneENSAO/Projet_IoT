async function loadLatest() {
    try {
        const res = await fetch("/latest/");
        const data = await res.json();

        document.getElementById("tempValue").textContent = data.temperature + " °C";
        document.getElementById("humValue").textContent = data.humidity + " %";

        const date = new Date(data.timestamp);
        const diffSec = Math.round((Date.now() - date) / 1000);

        document.getElementById("tempTime").textContent =
            "il y a : " + diffSec + " secondes (" + date.toLocaleTimeString() + ")";

        document.getElementById("humTime").textContent =
            "il y a : " + diffSec + " secondes (" + date.toLocaleTimeString() + ")";

    } catch (e) {
        console.log("Erreur API :", e);
    }
}

loadLatest();         // chargement initial
setInterval(loadLatest, 5000); // mise à jour toutes les 5 secondes
