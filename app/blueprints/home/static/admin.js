document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal");
    const form = document.getElementById("form");
    const modalTitle = document.getElementById("modal-title");
    const tableContainer = document.getElementById("table-container");
    const nomeTabella = document.getElementById("nome-tabella");
    const listaTabelle = document.getElementById("lista-tabelle");

    const btnApriAggiungi = document.getElementById("apri-modal");
    const btnAnnulla = document.getElementById("annulla");

    // modale di aggiunta/modifica (toggle)
    const toggleModal = (show = true) => {
        if (show) {
            modal.classList.replace("hidden", "flex");
        } else {
            modal.classList.replace("flex", "hidden");
            form.reset();
            form.removeAttribute("data-mode");
            form.removeAttribute("data-id");
        }
    };

    // apertura modale
    btnApriAggiungi.addEventListener("click", () => {
        modalTitle.innerText = "Aggiungi Prodotto";
        toggleModal(true);
    });

    // chiusura modale
    btnAnnulla.addEventListener("click", () => toggleModal(false));

    // loading dinamico delle tabelle 
    const caricaTabella = async (tipo) => {
        nomeTabella.textContent = tipo;
        const url = `/admin/management/${tipo}`;
        const response = await fetch(url, {
            method: "GET",
            headers: { "Accept": "application/json" }
        });

        const data = await response.json();
        tableContainer.innerHTML = data.html;
    };

    listaTabelle.addEventListener("click", (e) => {
        const item = e.target.closest("li");
        if (item) {
            const tipo = item.getAttribute("data-tipo");
            caricaTabella(tipo);
        }
    });

    // delegazione evento sul container della tabella
    tableContainer.addEventListener("click", async (e) => {
        const btnEdit = e.target.closest("#btn-edit");
        const btnDelete = e.target.closest("#btn-delete");

        // modifica prodotto
        if (btnEdit) {
            const d = btnEdit.dataset;

            modalTitle.innerText = "Modifica Prodotto";
            form.setAttribute("data-mode", "modifica");
            form.setAttribute("data-id", d.id);

            // precomilazione form di modifica prima id mostrarlo
            document.getElementById("form-codice").value = d.codice;
            document.getElementById("form-nome").value = d.nome;
            document.getElementById("form-descrizione").value = d.descrizione;
            document.getElementById("form-prezzo").value = d.prezzo;
            document.getElementById("form-quantita").value = d.quantita;

            toggleModal(true);
        }

        // eliminazione prodotto
        if (btnDelete) {
            const id = btnDelete.dataset.id;
            const nome = btnDelete.dataset.nome;

            if (confirm(`Sei sicuro di voler eliminare definitivamente "${nome}"?`)) {
                try {
                    const response = await fetch(`/admin/management/prodotto/elimina/${id}`, {
                        method: "DELETE",
                        headers: {
                            "X-CSRF-Token": document.querySelector("meta[name=csrf-token]").content
                        }
                    });
                    const result = await response.json();

                    if (result.status === "success") {
                        caricaTabella(nomeTabella.textContent.toLowerCase());
                    } else {
                        alert("Errore durante l'eliminazione: " + result.message);
                    }
                } catch (error) {
                    console.error("Errore fetch eliminazione:", error);
                }
            }
        }
    });

    // submit form dinamico
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const mode = form.getAttribute("data-mode");
        const id = form.getAttribute("data-id");

        const url = mode === "modifica"
            ? `/admin/management/prodotto/modifica/${id}`
            : "/admin/management/prodotto/aggiungi";

        const payload = {
            codice: document.getElementById("form-codice").value,
            nome: document.getElementById("form-nome").value,
            descrizione: document.getElementById("form-descrizione").value,
            prezzo: document.getElementById("form-prezzo").value,
            quantita: document.getElementById("form-quantita").value
        };

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": document.querySelector("meta[name=csrf-token]").content
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (result.status === "success") {
                toggleModal(false);
                caricaTabella(nomeTabella.textContent.toLowerCase());
            } else {
                alert("Errore: " + (result.message || "Dati non validi"));
            }
        } catch (error) {
            console.error("Errore salvataggio:", error);
        }
    });

});