from werkzeug.security import generate_password_hash

from web import create_app, db
from web.api.models import User, QuizResult, UserKeyword
from web.quizzes.definitions import QUIZZES
from web.quizzes.service import generate_keywords


app = create_app()

#We start populating the DB with a bunch of fake users and information filled in for them
populate_users = [
    {
        "username": "charlie",
        "displayname": "charlie",
        "email": "charlie@student.uwa.edu.au",
        "password": "password",
        "languages": ["English"],
        "units": ["CITS3403", "CITS3002"]
    },
    {
        "username": "alex",
        "displayname": "Alex",
        "email": "alex@student.uwa.edu.au",
        "password": "password",
        "languages": ["English"],
        "units": ["CITS3403", "CITS3002"]
    },
    {
        "username": "sam",
        "displayname": "Sam",
        "email": "sam@student.uwa.edu.au",
        "password": "password",
        "languages": ["English", "Vietnamese"],
        "units": ["CITS3403"]
    },
    {
        "username": "jordan",
        "displayname": "Jordan",
        "email": "jordan@student.uwa.edu.au",
        "password": "password",
        "languages": ["English", "Mandarin"],
        "units": ["CITS3403", "CITS2200"]
    }
]

#This sets out the quiz answers for the generated users
populated_user_answers = {
    "charlie": {
        "food_preferences": [5, 4, 3, 5, 3, 3, 5, 3, 5, 3],
        "social_energy": [4, 4, 4, 3, 4, 2, 2, 2, 2, 2],
        "communication_style": [3, 4, 4, 4, 4, 5, 4, 2, 2, 4]
    },
    "alex": {
        "food_preferences": [5, 4, 4, 5, 3, 3, 4, 3, 5, 4],
        "social_energy": [4, 5, 4, 3, 4, 2, 2, 1, 2, 2],
        "communication_style": [3, 4, 5, 4, 4, 5, 4, 2, 2, 5]
    },
    "sam": {
        "food_preferences": [1, 1, 2, 1, 2, 1, 1, 2, 1, 2],
        "social_energy": [1, 1, 1, 1, 1, 5, 5, 5, 5, 5],
        "communication_style": [5, 1, 1, 1, 1, 2, 1, 5, 5, 1]
    },
    "jordan": {
        "food_preferences": [4, 4, 3, 4, 3, 3, 4, 3, 4, 3],
        "social_energy": [3, 4, 3, 3, 3, 3, 2, 3, 2, 3]
    }
}

#This function then actually creates the users using our fake data
def create_populate_users():
    #We loop through each fake user and check if their username already exists in the DB
    for user_data in populate_users:
        existing_user = User.query.filter_by(username=user_data["username"]).first()

        #If the user already exists, we simply update their details rather then delete
        if existing_user:
            existing_user.displayname = user_data["displayname"]
            existing_user.email = user_data["email"]
            existing_user.password = generate_password_hash(user_data["password"])
            existing_user.languages = user_data["languages"]
            existing_user.units = user_data["units"]
            existing_user.reset_token_version = 0

        #If the user does not exist, we just add the user to the DB alongisde their fields
        else:
            user = User(
                username=user_data["username"],
                displayname=user_data["displayname"],
                email=user_data["email"],
                password=generate_password_hash(user_data["password"]),
                languages=user_data["languages"],
                units=user_data["units"],
                reset_token_version=0
            )
            #We then add the user to the DB
            db.session.add(user)
    #And here we save all the user changes in the DB
    db.session.commit()

#This function deletes any old quiz answers or information for the fake users
#This makes the function safe to run multiple times
def clear_populated_quiz_data():
    #We create a list of usernames
    populated_usernames = [user["username"] for user in populate_users]

    #We then delete all quiz results that belong to the populated fake users
    QuizResult.query.filter(
        QuizResult.username.in_(populated_usernames)
    ).delete(synchronize_session=False)

    #We also delete all the keywords associated with those users
    UserKeyword.query.filter(
        UserKeyword.username.in_(populated_usernames)
    ).delete(synchronize_session=False)

    #We then save the deletions in the DB
    db.session.commit()

    #This is a helper function that just converts the quiz answer list into a format the quiz service expects
def convert_answer_list_to_dict(answer_list):
    #We first create an empty dictionary
    answers = {}

    #We then loop through the quiz answers starting at question 1
    for index, score in enumerate(answer_list, start=1):
        #We then store each into the dictionary where each question number is a string
        answers[str(index)] = score

    #Finally we return the dictionary
    return answers

#This function saves a fake users answer for one quiz
def save_populated_quiz_attempt(username, quiz_name, answer_list):
    #We get the quiz titles first
    quiz = QUIZZES[quiz_name]
    #Then we use the helper function to convert the quiz answers
    answers = convert_answer_list_to_dict(answer_list)

    #We loop through each question in the quiz
    for question in quiz["questions"]:
        #And we get the question number
        question_index = question["question_index"]

        #And for each question we create a QuizResult row for that user and their answers for that quiz
        quiz_result = QuizResult(
            username=username,
            quiz_name=quiz_name,
            question_index=question_index,
            score=int(answers[str(question_index)])
        )   

        #We then add the quiz results to the DB
        db.session.add(quiz_result)

    #This then runs our existing keyword generation logic using the quizzes and their answers provided here
    generated_keywords = generate_keywords(quiz, answers)

    #We then loop through every keyword the user has generated for the quiz and we create an object for it to go into the DB
    for keyword in generated_keywords:
        user_keyword = UserKeyword(
            username=username,
            keyword=keyword,
            source_quiz=quiz_name
        )

        #We then add the keywords into the DB 
        db.session.add(user_keyword)