document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#forgot-form");
    const url = form.getAttribute("action");

    const risultato = document.querySelector("#result-error");
    if (risultato) {
        setTimeout(() => {
            risultato.classList.add("hidden");
        }, 5000);
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);

        const data = {
            email: (formData.get("email")).trim()
        }

        const result = await apiRequest(url, "POST", data);

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

                break;

            case "warning":
                flash.classList.add("bg-yellow-400");
                flashIcon.className = "bi-exclamation-triangle-fill";
                flashMessage.textContent = result.message;
                flash.classList.remove("hidden");

                setTimeout(() => {
                    flash.classList.add("hidden");
                    flash.classList.remove("bg-yellow-400");
                    flashMessage.textContent = "";
                }, 3000);

                break;

            case "error":
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

                break;
        }
    });
});