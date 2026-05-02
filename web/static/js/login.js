// Clear form input fields when swap between login and forgot password forms
function clearForm(formId) {
    const form = document.querySelector(`#${formId} form`);
    if (!form) return;

    form.reset();

    const flash = form.querySelector(".flash-alert");
    if (flash) flash.remove();
}

// Show forgot password form and hide login form
function showForgot(e) {
    if (e) e.preventDefault();

    clearForm("forgotForm");

    const login = document.getElementById("loginForm");
    const forgot = document.getElementById("forgotForm");

    login.classList.remove("active");
    forgot.classList.add("active");
}

// Show login form and hide forgot password form
function showLogin(e) {
    if (e) e.preventDefault();

    clearForm("loginForm");

    const login = document.getElementById("loginForm");
    const forgot = document.getElementById("forgotForm");

    forgot.classList.remove("active");
    login.classList.add("active");
}

// Validate email format for student emails only
function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@student\.uwa\.edu\.au$/;
    return regex.test(email);
}

// Handle forgot password form submission
document.querySelector("#forgotForm form").addEventListener("submit", function(e) {
    e.preventDefault();

    const formData = new FormData(this);

    showLogin();

    const flashArea = document.getElementById("flash-area");
    flashArea.innerHTML = `
                            <div class="alert alert-info text-center mt-2">
                                Check your email (may take a few seconds)
                            </div>
                        `;

    const alertBox = flashArea.querySelector(".alert");
    setTimeout(() => {
        alertBox.classList.add("flash-hide");  
    }, 3000);

    setTimeout(() => {
        flashArea.innerHTML = "";  
    }, 3000);

    fetch("/auth/forgot-password", {
        method: "POST",
        body: formData
    }).catch(err => {
        flashArea.innerHTML = `
            <div class="alert alert-danger text-center mt-2">
                Failed to send email
            </div>
        `;
    });
});