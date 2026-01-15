document.addEventListener("DOMContentLoaded", () => {
    const grigliaProdotti = document.querySelector("#griglia-prodotti");
    const carrello = document.querySelector("#carrello");
    const contaElementi = document.querySelector("#conta-elementi");

    aggiornaBadge(0);

    // funzione per aggiornare badge
    function aggiornaBadge(conteggio) {
        contaElementi.textContent = conteggio;
        if (parseInt(conteggio) === 0) {
            contaElementi.classList.add("hidden");
        } else {
            contaElementi.classList.remove("hidden");
        }
    }

    // funzione di sincronizzazione conteggio disponibilita
    function sincronizzaDisponibilita(id, delta) {
        const article = document.querySelector(`article[data-id="${id}"]`);

        if (!article) return;

        // variabile di conteggio presa con il data-attribute nel rendering iniziale
        let disponibili = parseInt(article.getAttribute("data-quantita"));

        // update e modifica realtime
        disponibili += delta;
        article.setAttribute("data-quantita", disponibili);

        const quantitaProdotto = article.querySelector("p.conteggio");

        if (quantitaProdotto) {
            quantitaProdotto.innerHTML = `<span class="font-semibold">Quantità: </span>${disponibili}`;
        }
    };

    grigliaProdotti.addEventListener("click", async (e) => {
        if (e.target.matches(".aggiungi")) {
            const article = e.target.closest("article");
            const id = article.getAttribute("data-id");
            const disponibili = parseInt(article.getAttribute("data-quantita"));

            if (disponibili <= 0 || disponibili - 1 < 0) {
                alert("Non ci sono piu prodotti disponibili");
                return;
            }

            const result = await apiRequest(`/carrello/aggiungi/${id}`, "POST", id);

            if (result.status === "success") {
                carrello.innerHTML = result.html;
                aggiornaBadge(result.conta_prodotti);
                sincronizzaDisponibilita(id, -1);
            } else {
                alert(result.message);
            }
        }
    })

    carrello.addEventListener("click", async (e) => {
        if (e.target.matches("#svuota")) {
            const itemsInCart = carrello.querySelectorAll("li[data-id]");
            const recupera = Array.from(itemsInCart).map(item => ({
                id: item.getAttribute("data-id"),
                quantita: parseInt(item.getAttribute("data-quantita"))
            }));

            const result = await apiRequest("/carrello/svuota", "POST");

            if (result.status === "success") {
                carrello.innerHTML = result.html;
                aggiornaBadge(0);
                recupera.forEach(item => {
                    sincronizzaDisponibilita(item.id, item.quantita);
                });
            }
            return;
        }

        const li = e.target.closest("li");
        if (!li) return;

        const id = li.getAttribute("data-id");
        const quantitaCarrello = parseInt(li.getAttribute("data-quantita"));

        const article = document.querySelector(`article[data-id="${id}"]`);
        const scorta = article ? parseInt(article.getAttribute("data-quantita")) : 0;

        let endpoint = null;
        let nuovaQuantitaCarrello = quantitaCarrello;
        let variazioneMagazzino = 0;

        if (e.target.matches(".incrementa")) {
            if (scorta <= 0 || scorta - 1 < 0) {
                alert("Non ci sono piu prodotti disponibili");
                return;
            }
            endpoint = `/carrello/modifica/${id}`;
            nuovaQuantitaCarrello = quantitaCarrello + 1;
            variazioneMagazzino - 1;
            sincronizzaDisponibilita(id, -1);

        } else if (e.target.matches(".decrementa")) {
            endpoint = `/carrello/modifica/${id}`;
            nuovaQuantitaCarrello = quantitaCarrello - 1;
            variazioneMagazzino + 1;
            sincronizzaDisponibilita(id, 1);

        } else if (e.target.matches(".elimina")) {
            endpoint = `/carrello/elimina/${id}`;
            variazioneMagazzino = quantitaCarrello;
            sincronizzaDisponibilita(id, scorta);
        }

        if (endpoint) {
            const result = await apiRequest(endpoint, "POST", { "id": id, "quantita": nuovaQuantitaCarrello });
            if (result.status === "success") {
                carrello.innerHTML = result.html;
                aggiornaBadge(result.conta_prodotti);
                sincronizzaDisponibilita(id, variazioneMagazzino);
            } else {
                alert(result.message);
            }
        }
    });

})