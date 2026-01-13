document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("modal");
    const formContainer = document.getElementById("form-container");
    const formElement = document.getElementById("form");
    const tableContainer = document.getElementById("table-container");
    const modalTitle = document.getElementById("modal-title");
    const nomeTabella = document.getElementById("nome-tabella");

    // variabili globali per dinamicità totale
    let currentEndpoint = "";
    let currentResourceType = "";

    // toggle della modale
    const toggleModal = (show = true) => {
        if (show) {
            modal.classList.replace("hidden", "flex");
        } else {
            modal.classList.replace("flex", "hidden");
            formElement.reset();
            formElement.removeAttribute("data-mode");
            formElement.removeAttribute("data-id");
        }
    };


    // caricamento dinamico della risorsa
    const caricaRisorsa = async (tipo) => {
        currentResourceType = tipo;
        nomeTabella.textContent = tipo.toUpperCase();

        try {
            // fetch dinamico all'endpoint corrispondente
            const response = await fetch(`/admin/api/load/${tipo}`);
            const data = await response.json();

            if (data.status === "success") {
                // display dinamico tabella selezionata
                tableContainer.innerHTML = data.table_html;

                // display dinamico form correlato
                formContainer.innerHTML = data.form_html;

                // update della variabile dell'endpoint
                currentEndpoint = data.endpoint;
            } else {
                console.error(data.message || "Errore nel caricamento della risorsa");
            }
        } catch (error) {
            console.error("Errore fetch:", error);
        }
    };

    // selezione tabella con event delegation sula lista
    document.getElementById("lista-tabelle").addEventListener("click", (e) => {
        const item = e.target.closest("li");
        if (item && item.hasAttribute("data-tipo")) {
            const tipo = item.getAttribute("data-tipo");
            caricaRisorsa(tipo);
        }
    });

    // delegazione eventi modifica/elimina sul container della tabella
    tableContainer.addEventListener("click", async (e) => {
        const btnEdit = e.target.closest(".btn-edit");
        const btnDelete = e.target.closest(".btn-delete");

        // modifica elemento dinamica
        if (btnEdit) {
            const id = btnEdit.dataset.id;
            const rowData = JSON.parse(btnEdit.dataset.row);

            modalTitle.textContent = `Modifica ${currentEndpoint}`;
            formElement.setAttribute("data-mode", "modifica");
            formElement.setAttribute("data-id", id);

            // compilazione dinamica del form in fase di modifica
            for (const [key, value] of Object.entries(rowData)) {
                const input = formElement.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = value;
                }
            }
            toggleModal(true);
        }

        // eliminazione elemento dinamico
        if (btnDelete) {
            const id = btnDelete.dataset.id;
            if (confirm("Sei sicuro di voler eliminare questo elemento?")) {
                await fetch(`/admin/management/${currentEndpoint}/elimina/${id}`, {
                    method: "DELETE",
                    headers: { "X-CSRF-Token": document.querySelector("meta[name=csrf-token]").content }
                });
                // caricaRisorsa(currentResourceType); reload page
            }
        }
    });

    // apertura modale
    document.getElementById("apri-modal").addEventListener("click", () => {
        modalTitle.textContent = `Aggiungi ${currentEndpoint}`;
        toggleModal(true);
    });

    document.getElementById("annulla").addEventListener("click", () => toggleModal(false));

    // invio del form al server (POST)
    formElement.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Recupero dinamico dei dati dal form
        const formData = new FormData(formElement);

        // creazione json object con i dati del form
        const payload = Object.fromEntries(formData.entries());

        const mode = formElement.getAttribute("data-mode");
        const id = formElement.getAttribute("data-id");

        const baseUrl = `/admin/management/${currentEndpoint}`;
        const url = mode === "modifica" ? `${baseUrl}/modifica/${id}` : `${baseUrl}/aggiungi`;

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
                caricaRisorsa(currentResourceType);
            } else {
                alert("Errore: " + JSON.stringify(result.message));
            }
        } catch (error) {
            console.error("Errore submit:", error);
        }
    });

    caricaRisorsa("prodotti");
});