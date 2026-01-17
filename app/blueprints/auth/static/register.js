document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#register-form");
    const url = form.getAttribute("action");

    form.addEventListener("submit", async (e) => {
        // evita reload della pagina
        e.preventDefault();

        // feedback visivo elaborazione richiesta
        const btn = document.querySelector("#submit-btn");
        const btnText = document.querySelector("#btn-text");
        const btnSpinner = document.querySelector("#btn-spinner");

        btn.disabled = true;
        btnText.textContent = "Elaborazione...";
        btnSpinner.classList.remove("hidden");

        // recupera i dati del form e li mette in un oggetto
        const formData = new FormData(e.target);

        // preparazione dati per il fetch al backend
        const data = {
            username: (formData.get("username")).trim(),
            email: (formData.get("email")).trim(),
            password: (formData.get("password")).trim(),
            password2: (formData.get("password2")).trim(),
            ruolo: (formData.get("ruolo"))
        }

        const result = await apiRequest(url, "POST", data);

        btn.disabled = false;
        btnText.textContent = "Registrati";
        btnSpinner.classList.add("hidden");

        // se il client non riceve dati, è stato lanciato un errore dal backend (429)
        if (!result) return;

        const flash = document.querySelector("#flash");
        const flashIcon = document.querySelector("#message-icon")
        const flashMessage = document.querySelector("#message-text");

        switch (result.status) {
            case "success":
                flash.classList.add("bg-green-400");
                flashIcon.className = "bi-check-circle-fill"
                flashMessage.textContent = result.message;
                flash.classList.remove("hidden");

                break;

            case "warning":
                flash.classList.add("bg-yellow-400");
                flashIcon.className = "bi-exclamation-triangle-fill"
                flashMessage.textContent = result.message;
                flash.classList.remove("hidden");

                setTimeout(() => {
                    flash.classList.add("hidden");
                    flash.classList.remove("bg-yellow-400");
                    flashMessage.textContent = "";
                }, 5000);

                break;

            case "error":
                for (const [key, value] of Object.entries(result.message)) {
                    const errorElement = document.querySelector(`#${key}-error`);
                    errorElement.textContent = value;
                    errorElement.classList.remove("hidden");

                    setTimeout(() => {
                        errorElement.classList.add("hidden");
                    }, 10000);
                }

                break;
        }
    });
});