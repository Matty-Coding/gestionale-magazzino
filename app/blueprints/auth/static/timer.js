document.addEventListener("DOMContentLoaded", () => {
    const timer = document.querySelector("#timer");
    const loginUrl = timer.dataset.loginUrl;

    let seconds = parseInt(timer.textContent);

    const interval = setInterval(() => {
        seconds--;
        timer.textContent = seconds;

        if (seconds === 0) {
            clearInterval(interval);

            // redirect alla pagina di login
            window.location.href = loginUrl;
        }
    }, 1000);
});