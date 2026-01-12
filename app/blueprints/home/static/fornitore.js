document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#fornitore-data");
    const url = form.getAttribute("action");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);

        const data = {
            ragione_sociale: (formData.get("ragione_sociale")).trim(),
            partita_iva: (formData.get("partita_iva")).trim(),
            telefono: (formData.get("telefono")).trim()
        }

        const result = await apiRequest(url, "POST", data);

        if (!result) return;

        if (result.status === "success") {
            alert("I dati sono stati aggiornati con successo");
        } else {
            alert("I dati inseriti non sono corretti");
        }
    })
})