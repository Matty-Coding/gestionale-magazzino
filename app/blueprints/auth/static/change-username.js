document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.querySelector("#open-username-modal");
    const modal = document.querySelector("#modal-username");
    const closeBtn = document.querySelector("#annulla");
    const saveBtn = document.querySelector("#salva");
    const input = document.querySelector("#input-username");
    const displayUsername = document.querySelector("#username");

    const updateUrl = openBtn.getAttribute("data-url");

    // apri menu tendina con click
    const tendina = document.querySelector("#tendina");
    const apriMenu = document.querySelector("#apri-menu");
    const freccia = document.querySelector("#apri-menu i");
    const menu = document.querySelector("#menu");

    apriMenu.addEventListener("click", (e) => {
        e.stopPropagation();

        const isOpen = menu.classList.contains("opacity-100");

        if (!isOpen) {
            freccia.classList.add("rotate-180");
            menu.classList.remove("invisible", "opacity-0", "translate-y-2");
            menu.classList.add("visible", "opacity-100", "translate-y-0");
        } else {
            chiudiMenu();
        }
    });

    document.addEventListener("click", (e) => {
        if (!tendina.contains(e.target)) {
            chiudiMenu();
        }
    });

    function chiudiMenu() {
        freccia.classList.remove("rotate-180");
        menu.classList.remove("visible", "opacity-100", "translate-y-0");
        menu.classList.add("invisible", "opacity-0", "translate-y-2");
    }

    openBtn?.addEventListener("click", () => {
        modal.classList.remove("hidden");
        modal.classList.add("flex");
        input.focus();
    });

    const closeModal = () => {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
    };

    closeBtn?.addEventListener("click", closeModal);

    modal?.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });

    saveBtn?.addEventListener("click", async () => {
        const newName = input.value.trim();
        const currentName = displayUsername.textContent.trim();

        if (!newName || newName === currentName) {
            closeModal();
            return;
        }

        const data = { username: newName };
        console.log("ecco il nuovo username", newName)
        const result = await apiRequest(updateUrl, "POST", data);

        if (!result) return;

        if (result.status === "success") {
            displayUsername.textContent = newName;
            closeModal();

        } else {
            const errorBlock = document.querySelector("#errore");
            errorBlock.textContent = result.message;
            errorBlock.classList.remove("hidden");

            setTimeout(() => {
                errorBlock.classList.add("hidden");
            }, 3000);
        }
    });
});