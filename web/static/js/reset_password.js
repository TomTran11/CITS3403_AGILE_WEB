document.querySelector("form").addEventListener("submit", function(e) {
    const p1 = document.querySelector("input[name='password']").value;
    const p2 = document.querySelector("input[name='confirm_password']").value;

    if (p1 !== p2) {
        e.preventDefault();
        alert("Passwords do not match");
    }
});