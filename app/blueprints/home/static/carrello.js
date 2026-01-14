document.addEventListener("DOMContentLoaded", () => {
    const grigliaProdotti = document.querySelector("#griglia-prodotti");
    const carrello = document.querySelector("#carrello");
    const contaElementi = document.querySelector("#conta-elementi");

    let conta = parseInt(contaElementi.getAttribute("data-conta"));

    if (conta === 0) contaElementi.classList.add("hidden");

    grigliaProdotti.addEventListener("click", async (e) => {
        if (e.target.matches(".aggiungi")) {
            const article = e.target.closest("article");
            const id = article.getAttribute("data-id");
            let disponibili = article.getAttribute("data-quantita");

            disponibili = parseInt(disponibili);

            if (disponibili <= 0 || disponibili - 1 < 0) {
                alert("Non ci sono piu prodotti disponibili");
                return;
            } else if (disponibili - 1 >= 0) {
                disponibili--;
                article.setAttribute("data-quantita", disponibili);
            }

            const result = await apiRequest(`/carrello/aggiungi/${id}`, "POST", id);

            if (result.status === "success") {
                carrello.innerHTML = result.html;
                contaElementi.classList.remove("hidden");
                contaElementi.textContent = result.conta_prodotti;
            } else {
                alert(result.message);
            }
        }

    })

    carrello.addEventListener("click", async (e) => {
        if (e.target.matches("#svuota")) {
            const result = await apiRequest("/carrello/svuota", "POST");

            if (result.status === "success") {
                carrello.innerHTML = result.html;
                contaElementi.classList.add("hidden");
                contaElementi.textContent = result.conta_prodotti;
            }
            return;
        }

        const li = e.target.closest("li");
        const id = li.getAttribute("data-id");
        let quantita = li.getAttribute("data-quantita");

        let endpoint = null;

        if (e.target.matches(".incrementa")) {
            endpoint = `/carrello/modifica/${id}`;
            quantita++;

        } else if (e.target.matches(".decrementa")) {
            endpoint = `/carrello/modifica/${id}`;
            quantita--;
        } else if (e.target.matches(".elimina")) {
            endpoint = `/carrello/elimina/${id}`;
        }

        if (endpoint) {
            const result = await apiRequest(endpoint, "POST", { "id": id, "quantita": quantita });
            if (result.status === "success") {
                carrello.innerHTML = result.html;
                if (result.conta_prodotti === 0) {
                    contaElementi.classList.add("hidden");
                } else {
                    contaElementi.classList.remove("hidden");
                }
                contaElementi.textContent = result.conta_prodotti;
            } else {
                alert(result.message);
            }
        }
    });

})