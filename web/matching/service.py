from web.api.models import QuizResult

#This variable stores the minimum percentage needed between 2 users to be a match
#Users below the threshold will not be shown
matching_threshold = 70

#This function gets all the saved quiz answers for the selected user from the database
def get_answers_for_user(username):
    #This is the query that runs through the database in QUizResult where for each row it looks to match the selected username
    quiz_results = QuizResult.query.filter_by(username=username).all()

    #This is the dictionary that will store the users answers to a quiz
    quiz_answers = {}

    #We then loop through each quiz answer that the sleected user answered
    for result in quiz_results:
        #Then we create a unique key pair using the quiz name and question number for that quiz
        key = (result.quiz_name, result.question_index)
        #Finally we store the users score for that quiz question into our dictionary
        quiz_answers[key] = result.score

    #We then return the quiz answer dictionary
    return quiz_answers

#This is a helper runction that finds out every other user who has taken a quiz 
def get_all_other_users(username):
    #We launch a query into the database to get all the usernames of users who have taken a quiz that isnt our current selected user
    other_results = QuizResult.query.filter(
        QuizResult.username != username
    ).all()

    #We store all the unique usernames from our query into list
    usernames = []

    #This loops through every quiz result that belongs to other users
    for result in other_results:
        #If that user does not have their username in the list already, it is added in
        if result.username not in usernames:
            usernames.append(result.username)

    #Finally we return the list of usernames that have taken a quiz that can potentially be a match
    return usernames