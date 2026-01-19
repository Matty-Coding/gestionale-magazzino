const container = document.querySelector("#container-prodotti");
const paginazione = document.querySelector("#paginazione");
const precedente = document.querySelector("#precedente a");
const successiva = document.querySelector("#successiva a");
const precedenteMobile = document.querySelector("#precedente-mobile a");
const successivaMobile = document.querySelector("#successiva-mobile a");

// Variabili per la gestione dello swipe
let touchStartX = 0;
let touchEndX = 0;

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

            // logica loop infinito bidirezionale per la paginazione mobile
            precedenteMobile.href = `?page=${result.precedente || result.totale_pagine}`;
            successivaMobile.href = `?page=${result.successiva || 1}`;

            // logica loop infinito bidirezionale per la paginazione
            precedente.href = `?page=${result.precedente || result.totale_pagine}`;
            successiva.href = `?page=${result.successiva || 1}`;

            window.history.pushState({}, "", `?page=${numeroPagina}`);

            // Riporta lo scroll del container in alto quando cambia pagina
            container.scrollTo(0, 0);
        }
    } catch (error) {
        console.log(`Errore nel caricamento dei prodotti: ${error}`);
    }
}

// Funzione per calcolare la direzione dello swipe
function gestisciSwipe() {
    // delta 
    const sogliaMinima = 100;
    const differenza = touchStartX - touchEndX;

    if (Math.abs(differenza) > sogliaMinima) {
        if (differenza > 0) {
            const urlAvanti = new URL(successiva.href, window.location.origin);
            caricaProdotti(urlAvanti.searchParams.get("page"));
        } else {
            const urlIndietro = new URL(precedente.href, window.location.origin);
            caricaProdotti(urlIndietro.searchParams.get("page"));
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // utilizzo dei parametri passati nell'url dal server
    const params = new URLSearchParams(window.location.search);
    const page = params.get("page") || 1;
    caricaProdotti(page);

    // Listener per il touch sul container
    container.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    container.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        gestisciSwipe();
    }, { passive: true });
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
});