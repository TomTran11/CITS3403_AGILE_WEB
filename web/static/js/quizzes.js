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


//This loads the content for the specific quiz the user has selected, so the questions for the quiz
function loadSelectedQuiz(quizName) {
    const quizDisplay = document.getElementById("quiz-display");

    //We sent a GET request to get the questions for a specific quiz
    fetch(`/quizzes/${quizName}`)
        .then(response => {
            //We then convert the response into JSON
            return response.json().then(data => {
                return { ok: response.ok, data: data };
            });
        })
        //We then handle a situation where if the backend returned and error
        .then(result => {
            // If backend returned error
            if (!result.ok) {
                quizDisplay.innerHTML = `<p>${result.data.error}</p>`;
                return;
            }

            const quiz = result.data;

            //We then save the quiz data globally so it can be accessed
            currentQuizName = quizName;
            currentQuiz = quiz;
            currentQuestionIndex = 0;
            answers = {};

            //We then display the quiz info to the user based on the quiz they selected
            quizDisplay.innerHTML = `
                <h2>${quiz.quiz_name}</h2>
                <p>${quiz.description || ""}</p>
                <p>${quiz.questions.length} questions</p>
                <button id="begin-quiz">Begin Quiz</button>
            `;

            //Once the button is clicked, the quiz starts
            document
                .getElementById("begin-quiz")
                .addEventListener("click", showCurrentQuestion);
        })
        //This error handles situations where we cant load the quiz questions
        .catch(error => {
            quizDisplay.innerHTML = "<p>We couldn't load this quizzes questions, we apologise.</p>";
            console.error(error);
        });
}

//This function then formats exactly how each question will look to the user
function showCurrentQuestion() {
    const quizDisplay = document.getElementById("quiz-display");

    //This gets the current question
    const question = currentQuiz.questions[currentQuestionIndex];

    //This is a check to see if the question is the last one for the quiz
    const isLastQuestion =
        currentQuestionIndex === currentQuiz.questions.length - 1;

    //We then render the question's user interface for the user to interact with
    quizDisplay.innerHTML = `
        <div class="quiz-question">
            <p>Question ${currentQuestionIndex + 1} of ${currentQuiz.questions.length}</p>

            <h2>${question.text}</h2>

            <label for="answer-slider">Answer from 1 to 5 based on how strongly you feel about the question.:</label>
            <input id="answer-slider" type="range" min="1" max="5" value="3">

            <p>Selected score: <span id="selected-score">3</span></p>

            <button id="next-question">
                ${isLastQuestion ? "Submit Quiz" : "Next Question"}
            </button>
        </div>
    `;

    //We then get the slider and display the elements
    const slider = document.getElementById("answer-slider");
    const selectedScore = document.getElementById("selected-score");

    //As the user moves the slider, we update the display score for the question
    slider.addEventListener("input", () => {
        selectedScore.textContent = slider.value;
    });

    //This outlines what happens next after a user clicks either next or submit
    document.getElementById("next-question").addEventListener("click", () => {
        // We then save the answer and convert the index to string for JSON format
        answers[String(question.question_index)] = Number(slider.value);

        if (isLastQuestion) {
            //If the user is on the last question, we submit the quiz
            submitQuiz();
        } else {
            //If it is not the last question, we move onto the next question
            currentQuestionIndex += 1;
            showCurrentQuestion();
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