document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#update-form");
    const url = form.getAttribute("action");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // feedback visivo elaborazione richiesta
        const btn = document.querySelector("#submit-btn");
        const btnText = document.querySelector("#btn-text");
        const btnSpinner = document.querySelector("#btn-spinner");

        btn.disabled = true;
        btnText.textContent = "Elaborazione...";
        btnSpinner.classList.remove("hidden");

        const formData = new FormData(e.target);

        const data = {
            password: (formData.get("password")).trim(),
            password2: (formData.get("password2")).trim(),
        }

        const result = await apiRequest(url, "POST", data);

        btn.disabled = false;
        btnText.textContent = "Aggiorna";
        btnSpinner.classList.add("hidden");

        if (!result) return;

        const flash = document.querySelector("#flash");
        const flashIcon = document.querySelector("#message-icon");
        const flashMessage = document.querySelector("#message-text");

        switch (result.status) {
            case "success":
                flash.classList.add("bg-green-400");
                flashIcon.className = "bi-check-circle-fill"
                flashMessage.textContent = result.message;
                flash.classList.remove("hidden");

                setTimeout(() => {
                    window.location.href = result.redirect;
                }, 2000);

                break;

            case "error":
                for (const [key, value] of Object.entries(result.message)) {
                    const errorElement = document.querySelector(`#${key}-error`);
                    errorElement.textContent = value;
                    errorElement.classList.remove("hidden");

                    setTimeout(() => {
                        errorElement.classList.add("hidden");
                    }, 5000);
                }

                break;
        }
    });
});