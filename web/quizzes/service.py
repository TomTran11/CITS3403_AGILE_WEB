from web import db
from web.api.models import QuizResult, UserKeyword
from web.quizzes.definitions import QUIZZES

#Returns the available quiz names as keys in a dictionary
def get_quiz_names():
    return list(QUIZZES.keys())

#Returns the quiz dictionary (questions) by using the quizzes name
def get_quiz_by_name(quiz_name):
    return QUIZZES.get(quiz_name)

#We cannot trust the Front End to do all the validation checking so we do some ourselves
#Checks the quizzes answers are within the expected parameters
def validate_answers(quiz, answers):
    expected_questions = quiz["questions"]

    #Checks if the Front End sends the users answers as a dictionary to be processed
    if not isinstance(answers, dict):
        return False, "Answers must be sent as a dictionary."

    #For every question in the quiz, we must check some things
    for question in expected_questions:
        question_index = str(question["question_index"])

        #Checks if all questions are answered
        if question_index not in answers:
            return False, f"Missing answer for question {question_index}."

        #Question answer must be a number
        try:
            score = int(answers[question_index])
        except ValueError:
            return False, f"Score for question {question_index} must be a number."

        #Answer number must be within the 1-5 scoring scale
        if score < 1 or score > 5:
            return False, f"Score for question {question_index} must be between 1 and 5."

    return True, None

#Function to save the user's quiz results + generates their keywords based on answers
def save_quiz_answers(username, quiz_name, answers):
    quiz = QUIZZES.get(quiz_name)

    if not quiz:
        return False, "Quiz not found.", None

    #Calls and runs the validation function
    is_valid, error = validate_answers(quiz, answers)

    if not is_valid:
        return False, error, None

    #If a user has retaken a quiz, their old answers are removed before processing
    QuizResult.query.filter_by(
        username=username,
        quiz_name=quiz_name
    ).delete()

    #A users old keywords from a previous quiz are also removed before processing
    UserKeyword.query.filter_by(
        username=username,
        source_quiz=quiz_name
    ).delete()

    #We loop through each quiz question and stores it in the DB
    for question in quiz["questions"]:
        #Question number as an integer
        question_index = question["question_index"]
        #Converts users answer into integer -> answer keys in JSON are strings "1"
        score = int(answers[str(question_index)])

        #This creates a new databse object for one quiz answer
        quiz_result = QuizResult(
            username=username,
            quiz_name=quiz_name,
            question_index=question_index,
            score=score
        )

        #Finally we add the answers to the current DB entry
        #It is not permenantly saved yet at this point
        db.session.add(quiz_result)

    #This generates the users associated keywords based on their question answers
    generated_keywords = generate_keywords(username, quiz_name, quiz, answers)

    #This creates the new DB object for the user and their keyword
    for keyword in generated_keywords:
        user_keyword = UserKeyword(
            username=username,
            keyword=keyword,
            source_quiz=quiz_name
        )

        #Once again we add the object to the current DB session
        db.session.add(user_keyword)

    #This is where we commit the DB session objects to be saved permenantly in the DB
    db.session.commit()

    return True, "Quiz submitted successfully.", generated_keywords

#Function to decide how to generate keywords for a user based on the quiz type
def generate_keywords(username, quiz_name, quiz, answers):
    generated_keywords = []

    #2 quiz types, direct and category
    #Direct quiz means a user can potentially have a keyword for each question
    if quiz["type"] == "direct":
        generated_keywords = generate_direct_quiz_keywords(quiz, answers)

    #Category quiz means a user can only get 1 keyword assigned at the end
    elif quiz["type"] == "category":
        category = calculate_category_result(quiz, answers)

        #If a keyword was found for a user, we add it to our empty list
        if category:
            generated_keywords.append(category)

    return generated_keywords

#Function to handle the direct quiz keywords
def generate_direct_quiz_keywords(quiz, answers):
    keywords = []

    #Looping through each question to figure out if a user gets a keyword and what
    for question in quiz["questions"]:
        question_index = question["question_index"]
        #Users score is needed to decide if a keyword is assigned or not
        score = int(answers[str(question_index)])

        #Extract the keyword assignment rules
        threshold = question.get("assign_keyword_if_score_at_least")
        keyword = question.get("keyword")

        #If keyword conditions are met for a question, the user gets that questions keyword
        if keyword and threshold and score >= threshold:
            keywords.append(keyword)

    return keywords

#Function to handle the category quiz keyword
def calculate_category_result(quiz, answers):
    #Starting score is 0
    total_score = 0

    #We then loop through each question to find what their final score is
    for question in quiz["questions"]:
        question_index = question["question_index"]
        score = int(answers[str(question_index)])

        if question.get("reverse_scored"):
            score = 6 - score

        total_score += score

    #We then loop through the quizzes category options and finds a category that the score fits into
    for category in quiz["categories"]:
        if category["min_score"] <= total_score <= category["max_score"]:
            return category["name"]

    return None