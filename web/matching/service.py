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

 #This function compares two users answers and then calculated their percentage match
def calculate_match_percentage(current_user_answers, other_user_answers):
    #This is a list that will store users that both users have answered
    overlapping_questions = []

    #We loop through every question answered by the current user
    for question_key in current_user_answers:
        #If that question has also been done by the other user
        if question_key in other_user_answers:
            #We add that question into our list 
            overlapping_questions.append(question_key)

    #If the users have both not done the same quiz, we return none as not match can be calculated
    if not overlapping_questions:
        return None, []

    #This variable stores the current total of the two users compatability
    total_compatibility = 0
    #This creates a list to store the name of quizzes that both users have completed
    shared_quizzes = []

    #For each question that both users answered, we get the current and other users score for the same question
    for question_key in overlapping_questions:
        current_score = current_user_answers[question_key]
        other_score = other_user_answers[question_key]

        #We then calculate the absolute difference between the two answered questions to calculate the differences in their scores
        difference = abs(current_score - other_score)
        #We then convert that difference value into a percentage
        #If both users answered 5 to the same question, their abs difference is 0, 1 - (0 / 4) = 1 which means their compatibility for the question is 100%
        #We divide the difference by 4 because 4 is the largest difference two users can have for the same question
        question_compatibility = 1 - (difference / 4)

        #We then add the questions compatibility score to the total compatability variable for the users
        total_compatibility += question_compatibility

        #We then split the unique key pair question_key back into its seperate fields
        quiz_name, question_index = question_key

        #We check if the quiz_name has already been recorded as a shared quiz between the two users
        if quiz_name not in shared_quizzes:
            #If not we append the shared quiz into out list
            shared_quizzes.append(quiz_name)

    #Finally, we use our total compatability variable and convert it into a percentage
    match_percentage = (total_compatibility / len(overlapping_questions)) * 100

    #We then return the final matching percentage rounded to 2 decimal places alongside the list of shared quizzes both users did
    return round(match_percentage, 2), shared_quizzes

#This is the main function that finds all the potential friend matches for a user based on the compatability score
def find_matches_for_user(username, threshold=matching_threshold):
    #For the current logged in user, we get all their answers for their quizzes
    current_user_answers = get_answers_for_user(username)

    #If the current user has not done any quizzes, we return an empty list as they cannot be matched with anyone
    if not current_user_answers:
        return []

    #This gets all the other users who have taken a quiz
    other_usernames = get_all_other_users(username)

    #This is an empty list that stores any and all potential matched for the current user
    matches = []

    #We then loop through every other user username
    for other_username in other_usernames:
        #And for each username, we get their quiz answers
        other_user_answers = get_answers_for_user(other_username)

        #We then compare the 2 users quiz answers using our helper function
        match_percentage, shared_quizzes = calculate_match_percentage(
            current_user_answers,
            other_user_answers
        )

        #If the two users have no overlapping quiz answers, cause they havnt both done the same quiz, we skip the current other user
        if match_percentage is None:
            continue

        #We then only include users as potential matches who are equal or higher than our matching threshold
        if match_percentage >= threshold:
            #We then add that user to our matches list alongside other information about them
            matches.append({
                "username": other_username,
                "match_percentage": match_percentage,
                #This is the number of quizzes both users have done
                "quizzes_compared": len(shared_quizzes),
                #This returns the quiz names that both users have done
                "shared_quizzes": shared_quizzes
            })

    #We then sort the matches from the highest and best match to the lowest
    matches.sort(
        key=lambda match: match["match_percentage"],
        reverse=True
    )

    #Finally we return the list of matches
    return matches