function $(id) { return document.getElementById(id); }

async function loadLatest() {
    try {
        // Récupérer la dernière mesure
        const resData = await fetch("/latest/");
        const data = await resData.json();

        if (data.timestamp) {
            $("temp").textContent = data.temperature.toFixed(1) + " °C";
            $("hum").textContent = data.humidity.toFixed(1) + " %";
            $("temp-time").textContent = "Dernière lecture: " + new Date(data.timestamp).toLocaleTimeString();
            $("hum-time").textContent = $("temp-time").textContent;
        }

        // Récupérer l'état de l'incident
        const resInc = await fetch("/incident/status/");
        const inc = await resInc.json();

        updateUI(inc);

    } catch (e) {
        console.error("Erreur de connexion au serveur", e);
    }
}

function updateUI(inc) {
    const badge = $("incident-badge");
    const counterSpan = $("incident-counter");

    counterSpan.textContent = inc.counter || 0;

    if (inc.is_open) {
        badge.className = "status-box alert";
        $("incident-status").textContent = "⚠️ INCIDENT EN COURS";

        // Affichage progressif des opérateurs
        $("op1").style.display = inc.counter >= 1 ? "block" : "none";
        $("op2").style.display = inc.counter >= 4 ? "block" : "none";
        $("op3").style.display = inc.counter >= 7 ? "block" : "none";

        // Remplir les données actuelles
        renderOpData(inc, "op1");
        renderOpData(inc, "op2");
        renderOpData(inc, "op3");

    } else {
        badge.className = "status-box ok";
        $("incident-status").textContent = "✅ Système Opérationnel";
        $("op1").style.display = "none";
        $("op2").style.display = "none";
        $("op3").style.display = "none";
    }
}

function renderOpData(inc, opPrefix) {
    const isAck = inc[opPrefix + "_ack"];
    $(opPrefix + "_ack").checked = isAck;
    $(opPrefix + "_show").textContent = inc[opPrefix + "_comment"] || "-";
    $(opPrefix + "_ack_status").textContent = isAck ? "Validé ✅" : "En attente...";
    $(opPrefix + "_ack_status").style.color = isAck ? "green" : "orange";
}

async function saveOperator(opNum) {
    const prefix = "op" + opNum;
    const ack = $(prefix + "_ack").checked;
    const comment = $(prefix + "_comment").value;

    const res = await fetch("/incident/update/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            op: opNum,
            ack: ack,
            comment: comment
        })
    });

    if (res.ok) {
        alert("Niveau " + opNum + " mis à jour !");
        loadLatest(); // Rafraîchir
    }
}

// Initialisation
document.addEventListener("DOMContentLoaded", () => {
    $("op1_save").onclick = () => saveOperator(1);
    $("op2_save").onclick = () => saveOperator(2);
    $("op3_save").onclick = () => saveOperator(3);

    loadLatest();
    setInterval(loadLatest, 5000);
});
