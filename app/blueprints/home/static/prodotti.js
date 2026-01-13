const container = document.querySelector("#container-prodotti");
const paginazione = document.querySelector("#paginazione");
const precedente = document.querySelector("#precedente a");
const successiva = document.querySelector("#successiva a");

async function caricaProdotti(numeroPagina) {
    if (!numeroPagina) return;

    try {
        const response = await fetch(`/prodotti?page=${numeroPagina}`, {
            method: "GET",
            headers: {
                "Accept": "application/json",
            }
        });

        const result = await response.json();

        if (result && result.html) {
            container.innerHTML = result.html;
            paginazione.textContent = `Pagina ${result.pagina_attuale} di ${result.totale_pagine}`;

            // logica loop infinito bidirezionale per la paginazione
            precedente.href = `?page=${result.precedente || result.totale_pagine}`;
            successiva.href = `?page=${result.successiva || 1}`;

            window.history.pushState({}, "", `?page=${numeroPagina}`);
        }
    } catch (error) {
        console.log(`Errore nel caricamento dei prodotti: ${error}`);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // utilizzo dei parametri passati nell'url dal server
    const params = new URLSearchParams(window.location.search);
    const page = params.get("page") || 1;
    caricaProdotti(page);
});

document.addEventListener("click", (e) => {
    const link = e.target.closest("a");
    if (link && link.href.includes("?page=")) {
        e.preventDefault();

        // aggiornamento dei parametri passati nell'url dal server
        const parametriUrl = new URLSearchParams(new URL(link.href).search);
        const numeroPagina = parametriUrl.get("page");
        caricaProdotti(numeroPagina);
    }
})