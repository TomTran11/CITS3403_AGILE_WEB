document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".flash-alert");

    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add("flash-hide");

            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 2000);
    });

    //Profile dropdown logic
    const profileBtn = document.querySelector(".profile-icon-btn");
    const dropdown = document.getElementById("profileDropdown");
    const menu = document.querySelector(".profile-menu");

    // Toggle dropdown
    if (profileBtn && dropdown) {
        profileBtn.addEventListener("click", (e) => {
            e.stopPropagation(); // prevent instant close
            dropdown.classList.toggle("open");
        });
    }

    //Close when clicking outside
    document.addEventListener("click", (e) => {
        if (menu && dropdown && !menu.contains(e.target)) {
            dropdown.classList.remove("open");
        }
    });
});