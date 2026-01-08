document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#register-form");
    const url = form.getAttribute("action");
    const csrfToken = document.querySelector("meta[name=csrf-token]").getAttribute("content");

    form.addEventListener("submit", async (e) => {
        // evita reload della pagina
        e.preventDefault();

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

        // fetch al backend
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": csrfToken
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            console.log(result);
        } catch (error) {
            console.error("Qualcosa è andato storto:", error);
        }
    })
})