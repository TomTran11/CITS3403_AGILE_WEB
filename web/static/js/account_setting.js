const openPasswordPopup = document.getElementById("openPasswordPopup");
const passwordPopup = document.getElementById("passwordPopup");
const cancelPopup = document.getElementById("cancelPopup");
const confirmSubmit = document.getElementById("confirmSubmit");

const accountSettingsForm = document.getElementById("accountSettingsForm");
const currentPasswordInput = document.getElementById("currentPasswordInput");
const currentPasswordHidden = document.getElementById("currentPasswordHidden");

const newPasswordInput = document.querySelector('input[name="new_password"]');
const confirmPasswordInput = document.querySelector('input[name="confirm_new_password"]');

if (
    openPasswordPopup &&
    passwordPopup &&
    cancelPopup &&
    confirmSubmit &&
    accountSettingsForm &&
    currentPasswordInput &&
    currentPasswordHidden &&
    newPasswordInput &&
    confirmPasswordInput
) {
    openPasswordPopup.addEventListener("click", function () {
        if (!accountSettingsForm.checkValidity()) {
            accountSettingsForm.reportValidity();
            return;
        }

        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (newPassword || confirmPassword) {
            if (newPassword !== confirmPassword) {
                alert("New password and confirm password do not match.");
                confirmPasswordInput.focus();
                return;
            }
        }

        passwordPopup.classList.add("show");
        currentPasswordInput.focus();
    });

    cancelPopup.addEventListener("click", function () {
        passwordPopup.classList.remove("show");
        currentPasswordInput.value = "";
    });

    confirmSubmit.addEventListener("click", function () {
        const currentPassword = currentPasswordInput.value.trim();

        if (!currentPassword) {
            alert("Please enter your current password.");
            return;
        }

        currentPasswordHidden.value = currentPassword;
        accountSettingsForm.submit();
    });
}