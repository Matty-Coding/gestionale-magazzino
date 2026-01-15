document.addEventListener("tabellaCaricata", function () {
    const searchInput = document.getElementById("search-input");
    const categoryButtons = document.querySelectorAll("#lista-categorie li[data-categoria]");
    const orderButtons = document.querySelectorAll("#lista-stati-ordine li[data-ordine]");

    const rows = document.querySelectorAll("tbody tr");

    // variabili globali (switch dinamici)
    let activeCategoryId = "all";
    let activeOrderStatus = "all";

    function applyFilters() {
        const searchTerm = searchInput.value.toLowerCase();

        rows.forEach(row => {
            const rowText = row.innerText.toLowerCase();

            // attributi di selezione per i filtri
            const rowCat = row.getAttribute("data-categoria");
            const rowStatus = row.getAttribute("data-info");

            const matchesSearch = rowText.includes(searchTerm);

            // filtro categoria (prodotti)
            const matchesCategory = (activeCategoryId === "all" || rowCat === activeCategoryId);

            // filtro stato (ordini)
            const matchesStatus = (activeOrderStatus === "all" || rowStatus === activeOrderStatus);

            // mostra solo selezionati
            if (matchesSearch && matchesCategory && matchesStatus) {
                row.classList.remove("hidden");
            } else {
                row.classList.add("hidden");
            }
        });
    }

    // filtri categoria prodotti
    categoryButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            const catId = this.getAttribute("data-categoria");
            activeCategoryId = (activeCategoryId === catId) ? "all" : catId;

            // toggle visivo
            categoryButtons.forEach(b => b.querySelector("button").classList.remove("bg-lime-500", "text-black"));
            if (activeCategoryId !== "all") this.querySelector("button").classList.add("bg-lime-500", "text-black");

            applyFilters();
        });
    });

    // filtri stato ordini
    orderButtons.forEach(btn => {
        btn.addEventListener("click", function () {
            const status = this.getAttribute("data-ordine");
            activeOrderStatus = (activeOrderStatus === status) ? "all" : status;

            // toggle visivo
            orderButtons.forEach(b => b.querySelector("button").classList.remove("bg-lime-500", "text-black"));
            if (activeOrderStatus !== "all") this.querySelector("button").classList.add("bg-lime-500", "text-black");

            applyFilters();
        });
    });

    // filtro ricerca tramite searchbar
    searchInput.addEventListener("input", applyFilters);
});