//This stores the selected quiz name
let currentQuizName = null;
//This stores the full quiz object that was returned by the backend
let currentQuiz = null;
//This tracks which question the user is doing
let currentQuestionIndex = 0;
//This stores the users quiz answers before being submitted to the backend
let answers = {};
//This stores and tracks which quizzes the user has done
let completedQuizNames = [];


//As soon as the page is loaded, we then load the quizzes
document.addEventListener("DOMContentLoaded", () => {
    loadQuizzes();

    document.getElementById("quiz-close-btn").addEventListener("click", closeModal);
    document.getElementById("quiz-overlay").addEventListener("click", (e) => {
        if (e.target === document.getElementById("quiz-overlay")) closeModal();
    });
});


//This functions loads all the quizzes and then splits them into the 2 sections, completed and todo
async function loadQuizzes() {
    const todoList = document.getElementById("todo-list");
    const completedList = document.getElementById("completed-list");
    const completedSection = document.getElementById("completed-section");

    try {
        //We then fetch the list of all the quiz names
        const namesRes = await fetch("/quizzes/");
        const NamesData = await namesRes.json();
        const quizNames = NamesData.quizzes;

        //Next we fetch all the quizzes that this user has completed
        let userCompleted =[];
        try {
            const completedRes = await fetch("/quizzes/completed");
            if (completedRes.ok) {
                const completedData = await completedRes.json();
                userCompleted = completedData.completed_quizzes || [];
            }
        //If the endpoint doesnt exist yet then the user has no completed quizzes and all of them are moved to the To-Do section
        } catch (_) {

        }

        completedQuizNames = userCompleted;

        //We then seperate the quizzes into two lists, one for completed quizzes and one for todo quizzes
        const todoNames = quizNames.filter(n => !userCompleted.includes(n));
        const doneNames = quizNames.filter(n => userCompleted.includes(n));

        //We then fill in the overall progress bar to show progress towards completing all quizzes for the user
        updateOverallProgress(doneNames.length, quizNames.length);

        //Next we create all the quiz cards that go in the todo section
        todoList.innerHTML = "";
        if (todoNames.length === 0) {
            todoList.innerHTML = "<p class='loading-text'>All quizzes completed!</p>";
        } else {
            todoNames.forEach(name => todoList.appendChild(buildCard(name, false)));
        }
 
        //Finally we create the quiz cards that go into the completed quiz section
        if (doneNames.length > 0) {
            completedSection.style.display = "block";
            completedList.innerHTML = "";
            doneNames.forEach(name => completedList.appendChild(buildCard(name, true)));
        }
 
    } catch (err) {
        todoList.innerHTML = "<p class='loading-text'>Could not load quizzes.</p>";
        console.error(err);
    }
}

//This function builds the quiz card element that goes into the sections
function buildCard(quizName, isCompleted) {
    const card = document.createElement("div");
    card.classList.add("quiz-card");
    if (isCompleted) card.classList.add("completed");
 
    //We have to get the quiz description so that we can place it onto the quiz card
    card.innerHTML = `
        <p class="quiz-card-name">${formatQuizName(quizName)}</p>
        <p class="quiz-card-desc">Loading...</p>
        <span class="quiz-card-badge ${isCompleted ? "" : "todo"}">${isCompleted ? "Completed ✓" : "Not started"}</span>`;
 
    //We then place the actual descriptions from the backend into the card
    fetch(`/quizzes/${quizName}`)
        .then(r => r.json())
        .then(data => {
            card.querySelector(".quiz-card-desc").textContent = data.description || "";
        })
        .catch(() => {
            card.querySelector(".quiz-card-desc").textContent = "";
        });
 
    //If the card is clicked and has been completed, we open the model that gives the user a summary of their previous answers, if not we open the quiz intro modal
    card.addEventListener("click", () => {
        if (isCompleted) {
            openChoiceModal(quizName);
        } else {
            openIntroModal(quizName);
        }
    });
 
    return card;
}

//This function is for the progress bar that goes at the bottom of the completed quiz section so that the user can see how far they have come from doing no quizzes
function updateOverallProgress(done, total) {
    const pct = total === 0 ? 0 : Math.round((done / total) * 100);
    document.getElementById("overall-progress-text").textContent = `${done} of ${total} quizzes completed`;
    document.getElementById("overall-progress-percent").textContent = `${pct}%`;
    document.getElementById("overall-progress-fill").style.width = `${pct}%`;
}

//These are all helper functions for the modal
//This opens the modal for the quiz and then disables the background page scrolling
function openModal() {
    document.getElementById("quiz-overlay").classList.add("active");
    document.body.style.overflow = "hidden";
}

//This closes the modal overlay and then restores the page scrolling whilst also hiding the modal progress bar that was there for a quiz
function closeModal() {
    document.getElementById("quiz-overlay").classList.remove("active");
    document.body.style.overflow = "";
    hideModalProgress();
}

//This cycles through the modals current HTML content as there are a variety of modal screens such as intro, question, results
function setModalContent(html) {
    document.getElementById("quiz-modal-content").innerHTML = html;
}
 
//This helper function displays and updates the modal progress bar that appears when a user begins taking a quiz
function showModalProgress(current, total) {
    const track = document.getElementById("modal-progress-track");
    const fill = document.getElementById("modal-progress-fill");
    const label = document.getElementById("modal-progress-label");

    //This makes the progress bar visible
    track.style.display = "block";
    //This updates the progress bar using a percentage to decide how filled the bar should be
    fill.style.width = `${(current / total) * 100}%`;
    //This then updates the progress bar text
    label.textContent = `${current} / ${total}`;
}

//The hides the modal's progress bar
function hideModalProgress() {
    document.getElementById("modal-progress-track").style.display = "none";
}

//This function sets out the introduction modal slide for when a user clicks on a quiz card
async function openIntroModal(quizName) {
    //We call the helper functions and open the modal
    openModal();
    //We then hide the progress bar as its only used when the user begins a quiz
    hideModalProgress();
    //We then show a temporary loading message to the user whilst we get the quiz data
    setModalContent(`<div class="modal-loading">Loading quiz...</div>`);

    try {
        //We then request the quiz data from the backend
        const res = await fetch(`/quizzes/${quizName}`);
        //We also must convert the JSON backend response into a JS object
        const quiz = await res.json();
 
        //We then store some of the quiz information globally to be used later
        currentQuizName = quizName;
        currentQuiz = quiz;
        currentQuestionIndex = 0;
        answers = {};
 
        //We then build the intro modal page with the follow headings and text
        setModalContent(`
            <div class="modal-intro">
                <p class="modal-quiz-name">${formatQuizName(quizName)}</p>
                <h2>How true are the following statements?</h2>
                <p>${quiz.description || ""}</p>
                <p class="modal-meta">${quiz.questions.length} questions &nbsp;·&nbsp; Rate each 1 to 5</p>
                <button class="modal-begin-btn" id="begin-btn">Let's Begin →</button>
            </div>
        `);
 
        //If the begin button is clicked, we then start the quiz
        document.getElementById("begin-btn").addEventListener("click", showQuestion);
    //If the quiz loading fails, we display an error message
    } catch (err) {
        setModalContent(`<div class="modal-loading">Could not load this quiz.</div>`);
        console.error(err);
    }
}

//This function sets out the modal slide for when a user clicks on a quiz card from their completed quiz section, meaning they have already done it
async function openChoiceModal(quizName) {
    //We use the helper functions again to open the modal and to also hide the progress bar as it is not needed here
    openModal();
    hideModalProgress();

    //We then build this modal page with the following headings and text
    setModalContent(`
        <div class="modal-choice">
            <p class="modal-quiz-name" style="font-size:0.8rem;letter-spacing:0.1em;text-transform:uppercase;opacity:0.8;margin-bottom:12px;">${formatQuizName(quizName)}</p>
            <h2>You've already completed this quiz.</h2>
            <p>Would you like to retake it and update your results, or view your previous keywords?</p>
            <div class="modal-choice-btns">
                <button class="btn-retake" id="choice-retake">Retake Quiz</button>
                <button class="btn-view-results" id="choice-view">View My Keywords</button>
            </div>
        </div>
    `);

    //If the user clicks the retake button, the quiz is started all over again
    document.getElementById("choice-retake").addEventListener("click", () => openIntroModal(quizName));
    //If the user clicks the keywords button, their saved keywords are shown
    document.getElementById("choice-view").addEventListener("click", () => viewKeywords(quizName));
}

//This allows the user to see their keywords that got assigned once they completed a quiz
async function viewKeywords(quizName) {
    //We set the loading message for the user
    setModalContent(`<div class="modal-loading">Loading your keywords...</div>`);
    //The progress bar is hidden as its irrelevant here
    hideModalProgress();
 
    try {
        //We request the saved keywords from the backend
        const res = await fetch(`/quizzes/${quizName}/keywords`);
        //If theres an error, we report it to the user
        if (!res.ok) throw new Error("Could not fetch keywords");
        //Then we convert the JSON response into a JS object
        const data = await res.json();
        //We then display the returned keyword
        showResultsSlide(data.keywords || [], quizName);
    //This is a error message for if the whole process fails
    } catch (err) {
        setModalContent(`<div class="modal-loading">Could not load your keywords.</div>`);
        console.error(err);
    }
}

//This sets out the modal slides for each question in a quiz that the user is currently doing
function showQuestion() {
    //We get the current question object based off the question index
    const question = currentQuiz.questions[currentQuestionIndex];
    //We then get the total number of questions in the current quiz
    const total = currentQuiz.questions.length;
    //This checks if the current question is the last question of not
    const isLast = currentQuestionIndex === total - 1;
 
    //This then updates and displays the progress bar for the quiz
    showModalProgress(currentQuestionIndex + 1, total);
 
    //We then create the quiz question content on the modal
    setModalContent(`
        <div class="modal-question">
            <p class="modal-quiz-name-small">${formatQuizName(currentQuizName)}</p>
            <p class="question-prompt">How true is the following statement?</p>
            <h2>${question.text}</h2>
            <div class="slider-row">
                <span class="slider-label">1</span>
                <input type="range" class="quiz-slider" id="q-slider" min="1" max="5" value="3">
                <span class="slider-label">5</span>
                <span class="slider-value-display" id="slider-val">3</span>
            </div>
            <button class="modal-next-btn" id="next-btn">
                ${isLast ? "Submit Quiz" : "Next →"}
            </button>
        </div>
    `);
 
    //We then disolay the question slider and value elements
    const slider = document.getElementById("q-slider");
    const valDisplay = document.getElementById("slider-val");
 
    //This updates the slider value live as the user drags it
    slider.addEventListener("input", () => {
        valDisplay.textContent = slider.value;
    });
 
    //This handles what happens when the user moves onto the next question
    document.getElementById("next-btn").addEventListener("click", () => {
        //We save the user selected answer using the question index as the key
        answers[String(question.question_index)] = Number(slider.value);
 
        //If the current question is the last one of the quiz, we submit the quiz
        if (isLast) {
            submitQuiz();
        } else {
            //Else we move onto the next question
            currentQuestionIndex++;
            showQuestion();
        }
    });
}

//This function submits the quiz after the user has completed it
async function submitQuiz() {
    const quizDisplay = document.getElementById("quiz-display");

    //Show loading message
    quizDisplay.innerHTML = `
        <h2>We are submitting your answers...</h2>
        <p>Please wait while your answers are saved and analysed.</p>
    `;

    //We then sent a POST request with the answers
    try {
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");
       
        const response = await fetch(`/quizzes/${currentQuizName}/submit`, {
            method: "POST",
            headers: {
                //We then tell the server that what we are sending is JSON
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                //We then convert the JS answers into a JSON string
                answers: answers
            })
        });

        //We then convert the backend's JSOn reponse into a JS object
        const result = await response.json();

        //This checks if the backends response was successful or not and displays an error message if needed
        if (!response.ok) {
            quizDisplay.innerHTML = `
                <h2>Error</h2>
                <p>${result.error}</p>
            `;
            return;
        }

        //This sends a request to the backend matching route
        const matchResponse = await fetch("/matching/");
        const matchData = await matchResponse.json();

        //We then create an empty string so that it can hold the suggested matches later on
        let matchesHtml = "";

        //We error check to see if the matching request failed or not
        if (!matchResponse.ok) {
            matchesHtml = "<p>We are so sorry but we could not load your potential matches.</p>";
        //This checks whether the request worked with no matches above the threshold meaning they have no acceptable matches
        } else if (matchData.matches.length === 0) {
            matchesHtml = "<p>We are so sorry, but there are no matches above the matching threshold yet.</p>";
        //Else the request worked and they have potential matches
        } else {
            //We start an unordered list for the matches and create a HTML block for each match
            matchesHtml = `
                <ul>
                    ${matchData.matches.map(match => `
                        <li>
                            <strong>${match.username}</strong>
                            — ${match.match_percentage}% match
                            <br>
                            Quizzes compared: ${match.quizzes_compared}
                            <br>
                            Shared quizzes: ${match.shared_quizzes.join(", ")}
                        </li>
                    `).join("")}
                </ul>
            `;
        }
        
        //We then replace the quizzes answering and display area with the final completed quiz display
        quizDisplay.innerHTML = `
            <h2>${result.message}</h2>
            <p>Your quiz has been completed and saved.</p>

            <h3>Generated keywords</h3>
            <ul>
                ${result.generated_keywords.map(keyword => `<li>${keyword}</li>`).join("")}
            </ul>

            <h3>Suggested Matches</h3>
            ${matchesHtml}
        `;
    //This error checks and catches any unexpected errors
    } catch (error) {
        quizDisplay.innerHTML = `
            <h2>An error has occured</h2>
            <p>We are so sorry, something has gone wrong with submitting the quiz.</p>
        `;
        console.error(error);
    }
}

//This is the helper function that helps format the quiz name to become more readable for the user
function formatQuizName(quizName) {
    return quizName
        //We replace all underscores with spaces and capitalise words
        .replaceAll("_", " ")
        .replace(/\b\w/g, letter => letter.toUpperCase());
}