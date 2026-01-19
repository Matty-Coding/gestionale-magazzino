// fetch centralizzato
async function apiRequest(url, method = "POST", data = {}) {
    const csrfToken = document
        .querySelector("meta[name='csrf-token']")
        .getAttribute("content");

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-CSRF-Token": csrfToken
            },
            body: JSON.stringify(data)
        });

        // intercettazione di flask limiter codice 429 > too many requests
        if (response.status === 429) {
            const errorData = await response.json();
            if (errorData.redirect) {
                window.location.href = errorData.redirect;
            }
            return null;
        }

        return await response.json();

    } catch (error) {
        // gestione di eventuali errori con la chiamata
        console.error("Errore nella chiamata API:", error);
        throw error;
    }
}

// setInterval(() => window.location.reload(), 5000);
