document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#login-form");
    const url = form.getAttribute("action");

    // esito risultato validazione email
    const risultati = document.querySelectorAll("#result-success, #result-error");
    risultati.forEach(risultato => {
        setTimeout(() => {
            risultato.classList.add("hidden");
        }, 5000);
    })

    form.addEventListener("submit", async (e) => {
        // evita reload della pagina
        e.preventDefault();

        // recupera i dati del form e li mette in un oggetto
        const formData = new FormData(e.target);

        // preparazione dati per il fetch al backend
        const data = {
            email: (formData.get("email")).trim(),
            password: (formData.get("password")).trim()
        }

        const result = await apiRequest(url, "POST", data);

        // se il client non riceve dati, è stato lanciato un errore dal backend (429)
        if (!result) return;

        const flash = document.querySelector("#flash");
        const flashIcon = document.querySelector("#message-icon");
        const flashMessage = document.querySelector("#message-text");

        switch (result.status) {
            case "success":
                flash.classList.add("bg-green-400");
                flashIcon.className = "bi-check-circle-fill";
                flashMessage.textContent = result.message;
                flash.classList.remove("hidden");

                setTimeout(() => {
                    // redirect alla dashboard
                    window.location.href = result.redirect;
                }, 1000);

                break;

            case "warning":
                flash.classList.add("bg-yellow-400");
                flashIcon.className = "bi-exclamation-triangle-fill";
                flashMessage.textContent = result.message;
                flash.classList.remove("hidden");

                setTimeout(() => {
                    flash.classList.add("hidden");
                    flashMessage.textContent = "";
                }, 3000);

                break;

            case "error":
                if (result.message === "Credenziali errate") {

                    flash.classList.add("bg-red-400");
                    flashIcon.className = "bi-exclamation-triangle-fill";
                    flashMessage.textContent = result.message;
                    flash.classList.remove("hidden");

                    setTimeout(() => {
                        flash.classList.add("hidden");
                        flash.classList.remove("bg-red-400");
                        flashIcon.className = "";
                        flashMessage.textContent = "";
                    }, 3000);

                } else {
                    for (const [key, value] of Object.entries(result.message)) {
                        const errorElement = document.querySelector(`#${key}-error`);
                        errorElement.textContent = value;
                        errorElement.classList.remove("hidden");

                        setTimeout(() => {
                            errorElement.classList.add("hidden");
                        }, 5000);
                    }
                }

                break;
        }
    });
});
