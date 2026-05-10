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

    // Notification dropdown logic
    const notifBtn = document.querySelector(".notif-btn");
    const notifDropdown = document.getElementById("notifDropdown");
    const notif = document.querySelector(".notif-menu");

    // Toggle profile dropdown
    if (profileBtn && dropdown) {
        profileBtn.addEventListener("click", (e) => {
            e.stopPropagation(); // prevent instant close
            dropdown.classList.toggle("open");

            if (notifDropdown) {
                notifDropdown.classList.remove("open");
            }
        });
    }

    // Toggle notification dropdown
    if (notifBtn && notifDropdown) {
        notifBtn.addEventListener("click", (e) => {
            e.stopPropagation();

            notifDropdown.classList.toggle("open");

            if (dropdown) {
                dropdown.classList.remove("open");
            }
        });
    }

    //Close when clicking outside
    document.addEventListener("click", (e) => {
        if (menu && dropdown && !menu.contains(e.target)) {
            dropdown.classList.remove("open");
        }

        if (notif && notifDropdown && !notif.contains(e.target)) {
            notifDropdown.classList.remove("open");
        }
    });
});