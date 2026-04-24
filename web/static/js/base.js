document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".flash-alert");

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add("flash-hide"); // fade out

            setTimeout(() => {
                alert.remove(); // remove after fade
            }, 500);
        }, 2000); // show for 2 seconds
    });
});