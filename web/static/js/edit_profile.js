document.addEventListener("DOMContentLoaded", () => {
    // =========================
    // Languages
    // =========================
    const languageSearch = document.getElementById("languageSearch");
    const languageDropdown = document.getElementById("languageDropdown");
    const selectedLanguagesBox = document.getElementById("selectedLanguages");
    const languagesData = document.getElementById("languagesData");

    if (languageSearch && languageDropdown && selectedLanguagesBox && languagesData) {
        let allLanguages = [];

        let selectedLanguages = languagesData.value
            ? languagesData.value.split(",").map(language => language.trim()).filter(Boolean)
            : [];

        function updateLanguagesHiddenInput() {
            languagesData.value = selectedLanguages.join(",");
        }

        function renderSelectedLanguages() {
            selectedLanguagesBox.innerHTML = "";

            if (selectedLanguages.length === 0) {
                selectedLanguagesBox.innerHTML = '<span class="tag-empty">No languages selected.</span>';
                return;
            }

            selectedLanguages.forEach(language => {
                const tag = document.createElement("span");
                tag.className = "tag tag-language";
                tag.textContent = language + " ×";

                tag.addEventListener("click", () => {
                    selectedLanguages = selectedLanguages.filter(item => item !== language);
                    updateLanguagesHiddenInput();
                    renderSelectedLanguages();
                });

                selectedLanguagesBox.appendChild(tag);
            });
        }

        function renderDropdown(searchText) {
            languageDropdown.innerHTML = "";

            if (!searchText.trim()) {
                return;
            }

            const matches = allLanguages
                .filter(language =>
                    language.toLowerCase().includes(searchText.toLowerCase()) &&
                    !selectedLanguages.includes(language)
                )
                .slice(0, 10);

            if (matches.length === 0) {
                const noResult = document.createElement("div");
                noResult.className = "language-option";
                noResult.textContent = "No matching language found";
                languageDropdown.appendChild(noResult);
                return;
            }

            matches.forEach(language => {
                const option = document.createElement("div");
                option.className = "language-option";
                option.textContent = language;

                option.addEventListener("click", () => {
                    selectedLanguages.push(language);
                    updateLanguagesHiddenInput();
                    renderSelectedLanguages();

                    languageSearch.value = "";
                    languageDropdown.innerHTML = "";
                });

                languageDropdown.appendChild(option);
            });
        }

        fetch("/api/languages")
            .then(response => response.json())
            .then(data => {
                allLanguages = data.languages;
                renderSelectedLanguages();
            })
            .catch(error => {
                console.error("Failed to load languages:", error);
            });

        languageSearch.addEventListener("input", () => {
            renderDropdown(languageSearch.value);
        });

        document.addEventListener("click", event => {
            if (!languageSearch.contains(event.target) && !languageDropdown.contains(event.target)) {
                languageDropdown.innerHTML = "";
            }
        });

        renderSelectedLanguages();
    }

    // =========================
    // Study Units
    // =========================
    const unitInput = document.getElementById("unitInput");
    const selectedUnitsBox = document.getElementById("selectedUnits");
    const unitsData = document.getElementById("unitsData");

    if (unitInput && selectedUnitsBox && unitsData) {
        let selectedUnits = unitsData.value
            ? unitsData.value.split(",").map(unit => unit.trim().toUpperCase()).filter(Boolean)
            : [];

        function updateUnitsHiddenInput() {
            unitsData.value = selectedUnits.join(",");
        }

        function renderSelectedUnits() {
            selectedUnitsBox.innerHTML = "";

            if (selectedUnits.length === 0) {
                selectedUnitsBox.innerHTML = '<span class="tag-empty">No study units selected.</span>';
                return;
            }

            selectedUnits.forEach(unit => {
                const tag = document.createElement("span");
                tag.className = "tag tag-unit";
                tag.textContent = unit + " ×";

                tag.addEventListener("click", () => {
                    selectedUnits = selectedUnits.filter(item => item !== unit);
                    updateUnitsHiddenInput();
                    renderSelectedUnits();
                });

                selectedUnitsBox.appendChild(tag);
            });
        }

        unitInput.addEventListener("keydown", event => {
            if (event.key === "Enter") {
                event.preventDefault();

                const unit = unitInput.value.trim().toUpperCase();

                if (!unit) {
                    return;
                }

                if (!/^[A-Z]{4}[0-9]{4}$/.test(unit)) {
                    alert("Invalid unit code. Use format like CITS3403.");
                    return;
                }

                if (!selectedUnits.includes(unit)) {
                    selectedUnits.push(unit);
                    updateUnitsHiddenInput();
                    renderSelectedUnits();
                }

                unitInput.value = "";
            }
        });

        renderSelectedUnits();
    }
});