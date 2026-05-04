function showFlash(message, type) {
    const flashArea = document.getElementById("flash-area");

    const flash = document.createElement("div");
    let alertType = type === "success" ? "alert-success" : "alert-danger";
    flash.className = `alert ${alertType}`;
    flash.innerText = message;

    flashArea.innerHTML = "";
    flashArea.appendChild(flash);

    setTimeout(() => {
        flash.remove();
    }, 3000);
}

document.getElementById("socialForm").addEventListener("submit", function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch("/update_socials", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
            showFlash(data.message, "success");

            // Reset form fields
            document.getElementById("socialForm").reset();

            // Scroll to flash message
            document.getElementById("flash-area").scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        } else {
            showFlash("Something went wrong", "error");
        }
    })
    .catch(err => {
        console.error(err);
        showFlash("Server error", "error");
    });
});