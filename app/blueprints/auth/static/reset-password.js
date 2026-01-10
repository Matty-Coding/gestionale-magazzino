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
                flash.classList.add("bg-green-400");
                flashIcon.className = "bi-check-circle-fill";
                flashMessage.textContent = result.message;
                flash.classList.remove("hidden");

                setTimeout(() => {
                    window.location.href = result.redirect;
                }, 2000);

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