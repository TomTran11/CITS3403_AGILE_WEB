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
    if (!isMatch) {
        return;
    }

    const flashWrapper = document.querySelector(".flash-wrapper");

    if (!flashWrapper) {
        console.log("It's a match!");
        return;
    }

    const flashMessage = document.createElement("div");
    flashMessage.className = "alert alert-success text-center flash-alert";
    flashMessage.textContent = "It's a match! Notification added.";

    flashWrapper.appendChild(flashMessage);

    setTimeout(function() {
        flashMessage.classList.add("flash-hide");
    }, 2500);

    setTimeout(function() {
        flashMessage.remove();
    }, 3500);
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

        const flashWrapper = document.querySelector(".flash-wrapper");

        if (flashWrapper) {
            const errorMessage = document.createElement("div");
            errorMessage.className = "alert alert-danger text-center flash-alert";
            errorMessage.textContent = "Could not update like.";
            flashWrapper.appendChild(errorMessage);

            setTimeout(function() {
                errorMessage.remove();
            }, 3500);
        } else {
            alert("Could not update like.");
        }
    }
}


function setupHeartButtons() {
    const heartButtons = document.querySelectorAll(".heart-btn");

    heartButtons.forEach(function(button) {
        button.addEventListener("click", handleHeartClick);
    });
}


document.addEventListener("DOMContentLoaded", setupHeartButtons);