document.addEventListener("DOMContentLoaded", () => {
    const language_input = document.getElementById("languageInput");
    const dropdown_list = document.getElementById("dropdownList");
    window.selectedLanguages = new Set();
    const selectedContainer = document.getElementById("selectedLanguages");
    const clearBtn = document.getElementById("clear");
    const unitInput = document.getElementById("unitInput");
    const password = document.querySelector('input[name="password"]');
    const confirmPassword = document.querySelector('input[name="confirm_password"]');
    const form = document.querySelector("form");
    const emailInput = document.querySelector('input[name="email"]');

    // Erase all selected languages
    clearBtn.addEventListener("click", () => {
        selectedLanguages.clear();
        dropdown_list.style.display = "none";
        clearBtn.style.display = "none";
        renderTags();
    });

    // Fetch languages
    fetch("/api/languages")
        .then(res => res.json())
        .then(data => {

            dropdown_list.innerHTML = "";

            const languages = data.languages;
            languages.forEach(lang => {
                const div = document.createElement("div");
                div.textContent = lang;
                div.dataset.value = lang;

                dropdown_list.appendChild(div);
            });
        });

    // Create tags <-> selected languages
    function renderTags() {
        selectedContainer.innerHTML = "";

        selectedLanguages.forEach(lang => {
            const tag = document.createElement("div");
            tag.className = "lang_tag";

            tag.innerHTML = `
                ${lang} <span data-lang="${lang}">×</span>
            `;

            selectedContainer.appendChild(tag);
        });
    }

    // Show dropdown
    language_input.addEventListener("focus", () => {
        dropdown_list.style.display = "block";
    });

    // Click outside
    document.addEventListener("click", (e) => {
        if (!e.target.closest(".dropdown-container")) {
            dropdown_list.style.display = "none";
        }
    });

    // Select language
    dropdown_list.addEventListener("click", (e) => {
        if (e.target.dataset.value) {
            const lang = e.target.dataset.value;

            if (!selectedLanguages.has(lang)) {
                selectedLanguages.add(lang);
                renderTags();
            }

            clearBtn.style.display = selectedLanguages.size > 0 ? "inline-block" : "none";
            language_input.value = "";
            dropdown_list.style.display = "none";
        }
    });

    // Remove tag
    selectedContainer.addEventListener("click", (e) => {
        if (e.target.dataset.lang) {
            selectedLanguages.delete(e.target.dataset.lang);
            renderTags();
            clearBtn.style.display = selectedLanguages.size > 0 ? "inline-block" : "none";
        }
    });

    // Search
    language_input.addEventListener("input", () => {
        dropdown_list.style.display = "block";

        const filter = language_input.value.toLowerCase();
        const items = dropdown_list.querySelectorAll("div");

        items.forEach(item => {
            item.style.display = item.textContent.toLowerCase().includes(filter)
                ? "block"
                : "none";
        });
    });

    // UI / UX for password validation
        confirmPassword.addEventListener("input", () => {
            if (confirmPassword.value === "") {
                confirmPassword.style.border = "none";
            } else if (password.value === confirmPassword.value) {
                confirmPassword.style.border = "3px solid green";
            } else {
                confirmPassword.style.border = "3px solid red";
            }
        });
    
    // UI / UX for password validation
    emailInput.addEventListener("input", () => {
        const email = emailInput.value.trim();
        const regex = /^[a-zA-Z0-9._%+-]+@student\.uwa\.edu\.au$/;

        if (email === "") {
            emailInput.style.border = "none";
        } 
        else if (regex.test(email)) {
            emailInput.style.border = "3px solid green";
            emailInput.setCustomValidity("");
        } 
        else {
            emailInput.style.border = "3px solid red";
            emailInput.setCustomValidity("Must use @student.uwa.edu.au email");
        }
    });

    // Stop submission if unit code is invalid, password not the same as confirmed one and spoken languages requirement not met
    form.addEventListener("submit", (e) => {
        const email = emailInput.value.trim();
        const regex = /^[a-zA-Z0-9._%+-]+@student\.uwa\.edu\.au$/;
        if (!regex.test(email)) {
            e.preventDefault(); 
            emailInput.setCustomValidity("Must use @student.uwa.edu.au email");
            emailInput.reportValidity(); 
            return;
        } else {
            emailInput.setCustomValidity(""); 
        }

        if (selectedLanguages.size === 0) {
            e.preventDefault();
            alert("Please select at least one language.");
            return;
        }
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            alert("Passwords do not match.");
            return;
        }
    });

    
});