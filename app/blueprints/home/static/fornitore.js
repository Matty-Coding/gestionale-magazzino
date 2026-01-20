document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#fornitore-data");

    if (!form) return;

    const url = form.getAttribute("action");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = {
            ragione_sociale: (formData.get("ragione_sociale") || "").trim(),
            partita_iva: (formData.get("partita_iva") || "").trim(),
            telefono: (formData.get("telefono") || "").trim()
        };

        try {

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": document.querySelector("meta[name=csrf-token]")?.getAttribute("content")
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Errore del server: ${response.status}`);
            }

            const result = await response.json();
            console.log("Risultato ricevuto:", result);

            if (result && result.status === "success") {
                alert("I dati sono stati aggiornati con successo");
            } else {
                alert("I dati inseriti non sono corretti: " + (result.message || "Errore generico"));
            }

        } catch (error) {
            console.error("Si è verificato un errore durante il fetch:", error);
            alert("Errore di connessione o del server.");
        }
    });
});