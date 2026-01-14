document.addEventListener('tabellaCaricata', function () {
    const searchInput = document.getElementById('search-input');
    const categoryButtons = document.querySelectorAll('#lista-categorie li');
    const rows = document.querySelectorAll('tr[data-info]');
    let activeCategoryId = 'all';

    function applyFilters() {
        const searchTerm = searchInput.value.toLowerCase();
        rows.forEach(row => {
            const rowText = row.getAttribute('data-info');
            const rowCat = row.getAttribute('data-categoria');

            const matchesSearch = rowText.includes(searchTerm);
            const matchesCategory = (activeCategoryId === 'all' || rowCat === activeCategoryId);

            // toggle visibilità con tailwind class (hidden) dei risultati
            if (matchesSearch && matchesCategory) {
                row.classList.remove('hidden');
            } else {
                row.classList.add('hidden');
            }
        });
    }

    // eventi di selezione sui button delle categorie
    categoryButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const catId = this.getAttribute('data-categoria');

            // click su categoria attiva per disattivarla
            if (activeCategoryId === catId) {
                activeCategoryId = 'all';
                this.querySelector('button').classList.remove('bg-lime-500', 'text-black');
            } else {
                // stile focus su elementi non filtrati rimossi
                categoryButtons.forEach(b => b.querySelector('button').classList.remove('bg-lime-500', 'text-black'));

                // stile focus su elemento selezionato applicato
                activeCategoryId = catId;
                this.querySelector('button').classList.add('bg-lime-500', 'text-black');
            }

            applyFilters();
        });
    });

    // input dinamico per la ricerca
    searchInput.addEventListener('input', applyFilters);
});