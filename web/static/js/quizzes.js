//This stores the selected quiz name
let currentQuizName = null;
//This stores the full quiz object that was returned by the backend
let currentQuiz = null;
//This tracks which question the user is doing
let currentQuestionIndex = 0;
//This stores the users quiz answers before being submitted to the backend
let answers = {};


//As soon as the page is loaded, we then load the quizzes
document.addEventListener("DOMContentLoaded", () => {
    loadQuizzes();
});


//This functions loads all the quizzes
function loadQuizzes() {
    const quizList = document.getElementById("quiz-list");

    //We send a GET request to backend to get our quizzes
    fetch("/quizzes/")
        //We then also convert the responses into JSON
        .then(response => response.json())
        .then(data => {
            //If theres any existing content, we clear it
            quizList.innerHTML = "";

            //We then loop through each quiz name that was returned
            data.quizzes.forEach(quizName => {
                //For each available quiz we make a button for it
                const button = document.createElement("button");

                //We also format the quiz name to have better readability
                button.textContent = formatQuizName(quizName);

                //And we add a CSS class to the buttons so that can be styled
                button.classList.add("quiz-card");

                //When a specific button is clicked by a user, we load the quiz they selected
                button.addEventListener("click", () => {
                    loadSelectedQuiz(quizName);
                });

                //We then append the button we made to the quiz list container so the users can interact with it
                quizList.appendChild(button);
            });
        })
        //If the request fails, we inform the user of the error
        .catch(error => {
            quizList.innerHTML = "<p>Could not load quizzes.</p>";
            console.error(error);
        });
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
function submitQuiz() {
    const quizDisplay = document.getElementById("quiz-display");

    // Show loading message
    quizDisplay.innerHTML = `
        <h2>We are submitting your answers...</h2>
        <p>Please wait while your answers are saved and analysed.</p>
    `;

    //We then sent a POST request with the answers
    fetch(`/quizzes/${currentQuizName}/submit`, {
        method: "POST",
        headers: {
            //We then tell the server that what we are sending is JSON
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            //However we send the answers as objects
            answers: answers
        })
    })
        .then(response => {
            //We then convert the response to JSON and keep the current status
            return response.json().then(data => {
                return { ok: response.ok, data: data };
            });
        })
        .then(result => {
            //This handles the situation for when the backend returns an error
            if (!result.ok) {
                quizDisplay.innerHTML = `
                    <h2>Error</h2>
                    <p>${result.data.error}</p>
                `;
                return;
            }

            //We then display the success message to the user and their assigned keywords
            quizDisplay.innerHTML = `
                <h2>Thank you for completing the ${currentQuiz.quiz_name}!</h2>
                <p>Your answers are saved, and your keywords are being calculated.</p>

                <h3>Generated keywords</h3>
                <ul>
                    ${result.data.generated_keywords
                        .map(keyword => `<li>${keyword}</li>`)
                        .join("")}
                </ul>
            `;
        })
        //Error handling for when something goes wrong with quiz submission
        .catch(error => {
            quizDisplay.innerHTML = `
                <h2>Error</h2>
                <p>We're so sorry, something seems to have gone wrong with submitting your quiz.</p>
            `;
            console.error(error);
        });
}


//This is the helper function that helps format the quiz name to become more readable for the user
function formatQuizName(quizName) {
    return quizName
        //We replace all underscores with spaces and capitalise words
        .replaceAll("_", " ")
        .replace(/\b\w/g, letter => letter.toUpperCase());
}