document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#reset-form");
    const url = form.getAttribute("action");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);

        const data = {
            password: (formData.get("password")).trim(),
            password2: (formData.get("password2")).trim(),
        }

        const result = await apiRequest(url, "POST", data);

        if (!result) return;

        const flash = document.querySelector("#flash");
        const flashIcon = document.querySelector("#message-icon");
        const flashMessage = document.querySelector("#message-text");

        switch (result.status) {
            case "success":
                if (result.redirect) {
                    window.location.href = result.redirect;
                }

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
                if (result.message === "Link non valido o scaduto") {
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