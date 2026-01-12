document.addEventListener("DOMContentLoaded", () => {
    const openBtn = document.querySelector("#open-username-modal");
    const modal = document.querySelector("#modal-username");
    const closeBtn = document.querySelector("#annulla");
    const saveBtn = document.querySelector("#salva");
    const input = document.querySelector("#input-username");
    const displayUsername = document.querySelector("#username");

    const updateUrl = openBtn.getAttribute("data-url");

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