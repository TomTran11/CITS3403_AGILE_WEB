function getCsrfToken() {
    const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');

    if (!csrfMetaTag) {
        console.error("CSRF token meta tag not found.");
        return "";
    }

    return csrfMetaTag.getAttribute("content");
}


function getLikeUrl(username, alreadyLiked) {
    if (alreadyLiked) {
        return `/profile/${username}/unlike`;
    }

    return `/profile/${username}/like`;
}


function updateHeartButton(button, liked) {
    if (liked) {
        button.textContent = "♥";
        button.dataset.liked = "true";
        button.classList.add("liked");
    } else {
        button.textContent = "♡";
        button.dataset.liked = "false";
        button.classList.remove("liked");
    }
}


function showMatchMessage(isMatch) {
    if (isMatch) {
        alert("It's a match!");
    }
}


async function sendLikeRequest(username, alreadyLiked) {
    const csrfToken = getCsrfToken();
    const url = getLikeUrl(username, alreadyLiked);

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        }
    });

    if (!response.ok) {
        throw new Error("Like request failed");
    }

    return response.json();
}


async function handleHeartClick(event) {
    event.preventDefault();
    event.stopPropagation();

    const button = event.currentTarget;
    const username = button.dataset.username;
    const alreadyLiked = button.dataset.liked === "true";

    try {
        const data = await sendLikeRequest(username, alreadyLiked);

        updateHeartButton(button, data.liked);
        showMatchMessage(data.match);
    } catch (error) {
        console.error(error);
        alert("Could not update like.");
    }
}


function setupHeartButtons() {
    const heartButtons = document.querySelectorAll(".heart-btn");

    heartButtons.forEach(function(button) {
        button.addEventListener("click", handleHeartClick);
    });
}


document.addEventListener("DOMContentLoaded", function() {
    setupHeartButtons();
});