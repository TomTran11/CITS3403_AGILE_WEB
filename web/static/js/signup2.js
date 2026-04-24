document.addEventListener("DOMContentLoaded", () => {
    const unitInput = document.getElementById("unitInput");
    const selectedUnitsContainer = document.getElementById("selectedUnits");
    const eraseBtn = document.getElementById("erase");
    const form = document.querySelector("form");
    const alerts = document.querySelectorAll(".flash-alert");

    const selectedUnits = new Set();
    const regex = /^[A-Z]{4}[0-9]{4}$/;

    function renderUnits() {
        selectedUnitsContainer.innerHTML = "";

        selectedUnits.forEach(unit => {
            const tag = document.createElement("div");
            tag.className = "unit_tag";

            tag.innerHTML = `${unit} <span data-unit="${unit}">×</span>`;
            selectedUnitsContainer.appendChild(tag);
        });
    }

    selectedUnitsContainer.addEventListener("click", (e) => {
        if (e.target.dataset.unit) {
            selectedUnits.delete(e.target.dataset.unit);
            renderUnits();
        }
        eraseBtn.style.display = selectedUnits.size > 0 ? "inline-block" : "none";
    });

    // Add unit on Enter key
    unitInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();

            const unit = unitInput.value.trim().toUpperCase();
            if (!regex.test(unit)) {
                alert("Invalid unit (e.g. CITS3001)");
                return;
            }

            if (!selectedUnits.has(unit)) {
                selectedUnits.add(unit);
                renderUnits();
            }

            unitInput.value = "";
            eraseBtn.style.display = selectedUnits.size > 0 ? "inline-block" : "none";
            unitInput.style.border = "none";
        }
    });

    // UI / UX for unit code validation
    unitInput.addEventListener("input", () => {
        // auto uppercase
        unitInput.value = unitInput.value.toUpperCase();

        const regex = /^[A-Z]{4}[0-9]{4}$/;

        if (regex.test(unitInput.value)) {
            unitInput.style.border = "3px solid green";
        } else {
            unitInput.style.border = "3px solid red";
        }
    });

    // Erase all units
    eraseBtn.addEventListener("click", () => {
        selectedUnits.clear();
        renderUnits();
        eraseBtn.style.display = "none";
    });

    // Form submission
    form.addEventListener("submit", (e) => {
        if (selectedUnits.size === 0) {
            e.preventDefault();
            alert("Please add at least one unit.");
            return;
        }

        if (selectedLanguages.size === 0) {
            e.preventDefault();
            alert("Please select at least one language.");
            return;
        }

        // Validate format
        if (![...selectedUnits].every(unit => regex.test(unit))) {
            e.preventDefault();
            alert("Invalid unit (e.g. CITS3001)");
            return;
        }

        document.getElementById("unitsData").value = [...selectedUnits].join(",");
        document.getElementById("languagesData").value = [...selectedLanguages].join(",");
    });

    // Flash alert auto-hide
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add("flash-hide");

            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 2000); // show for 2 seconds
    });
});