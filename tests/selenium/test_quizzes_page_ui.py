"""
1. Quizzes page loads correctly
    1. Quiz cards appear
    2. Quiz card sections are clear and visible
    3. Overall progress bar shows correct progress amount

2. Completed Quiz Modal
    1. Clicking a quiz card in completed section opens a modal
    2. Modal opened has retake and view keywords buttons
    3. Clicking view keywords makes keywords modal summary appear
    4. Close modal button works properly
    5. Reopen the same completed quiz card
    6. Click the retake button instead
    7. Quiz question modal opens and complete the 10 questions
    8. Submit the quiz
    9. Result slide appears for the quiz
    10. Closing the modal from results slide

3. To-Do Quiz Flow
    1. Click a to-do quiz card
    2. Check that the intro modal slide appears with quiz description and begin quiz button
    3. Clicking begin goes into the question modal with the question and slider
    4. Slider works to answer all 10 questions by clicking the next button
    5. Last question submit button works properly
    6. The results slide appears afterwards

4. After Quiz Submission
    1. Modal close button works
    2. Check the just completed to-do quiz has moved to the completed section
    3. Check that the overall progress bar has been updated
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5000"

#Helper functions to make running the rest of the tests more streamlined
#This function logs in the user using one of our fake users
def login_user(driver, username="charlie", password="password"):
    driver.get(f"{BASE_URL}/auth/login")
    time.sleep(2)
    login_form = driver.find_element(By.ID, "loginForm")
    login_form.find_element(By.NAME, "username").send_keys(username)
    login_form.find_element(By.NAME, "password").send_keys(password)
    login_form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

#THis function simply navigates to the quizzes page after logging in
def go_to_quizzes(driver):
    driver.get(f"{BASE_URL}/quizzes/page")
    time.sleep(2)

#This helper function closes the current modal slide that were in
def close_modal(driver):
    driver.find_element(By.ID, "quiz-close-btn").click()
    time.sleep(1)

#This function just moves the question slider in the question modals
def set_slider_value(driver, value):
    slider = driver.find_element(By.ID, "q-slider")
    driver.execute_script("arguments[0].value = arguments[1];", slider, value)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input'));", slider)

#This helper function just answers all the quiz questions when we begin a quiz
def answer_all_questions(driver, q1_value=5, q10_value=4, default_value=3):
    for i in range(10):
        if i == 0:
            set_slider_value(driver, q1_value)
        elif i == 9:
            set_slider_value(driver, q10_value)
        else:
            set_slider_value(driver, default_value)
        
        next_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "next-btn"))
        )
        next_btn.click()
        time.sleep(0.5)

#We firstly check if the quiz page loads correctly when navigated too
def test_quizzes_page_loads_correctly(driver):
    #Helper functions are used to login and navigate to the page
    login_user(driver)
    go_to_quizzes(driver)

    #We wait for the quiz cards to load into their sections
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz-card"))
    )

    #We then check that both sections are visible
    assert driver.find_element(By.ID, "completed-section").is_displayed()
    assert driver.find_element(By.ID, "todo-section").is_displayed()

    #We check that each section has quiz cards in them
    assert len(driver.find_elements(By.CSS_SELECTOR, "#completed-list .quiz-card")) > 0
    assert len(driver.find_elements(By.CSS_SELECTOR, "#todo-list .quiz-card")) > 0

    #We also check that the overall progress bar is visible and shows the progress text
    assert driver.find_element(By.CSS_SELECTOR, ".overall-progress-section").is_displayed()
    assert "quizzes completed" in driver.find_element(By.ID, "overall-progress-text").text

##We then test the modal flow for when we click on a quiz card in the completed section
def test_completed_quiz_modal_flow(driver):
    #We use our helper functions to login and navigate to the page
    login_user(driver)
    go_to_quizzes(driver)

    #We then wait until the quiz cards appear in the completed list section
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#completed-list .quiz-card"))
    )

    #We then click on a completed quiz card
    driver.find_elements(By.CSS_SELECTOR, "#completed-list .quiz-card")[0].click()
    time.sleep(1)

    #A modal should then open and we confirm that it does and that 2 buttons are present, retake and view results
    assert "active" in driver.find_element(By.ID, "quiz-overlay").get_attribute("class")
    assert driver.find_element(By.CSS_SELECTOR, ".btn-retake").is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, ".btn-view-results").is_displayed()

    #We first check if the view results button works but clicking on it
    driver.find_element(By.CSS_SELECTOR, ".btn-view-results").click()
    time.sleep(1)

    #We then check to see if the key words are displayed properly
    assert driver.find_element(By.CSS_SELECTOR, ".modal-results").is_displayed()
    assert len(driver.find_elements(By.CSS_SELECTOR, ".keyword-chip")) > 0

    #Next we close the modal
    close_modal(driver)
    time.sleep(1)

    #And click to reopen the exact same quiz card and check the other button option
    driver.find_elements(By.CSS_SELECTOR, "#completed-list .quiz-card")[0].click()
    time.sleep(1)

    #We click the other button to retake the quiz
    driver.find_element(By.CSS_SELECTOR, ".btn-retake").click()
    time.sleep(1)

    #We then check that a modal opens and that it is the question modal as we move to retake the quiz
    assert driver.find_element(By.CSS_SELECTOR, ".modal-question").is_displayed()
    #We also check to see if the question slider appears
    assert driver.find_element(By.ID, "q-slider").is_displayed()

    #Next we call the helper function to complete all the quiz questions
    answer_all_questions(driver)

    #After the quiz is finished we then confirm that the results modal slide is showed
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-results"))
    )
    assert driver.find_element(By.CSS_SELECTOR, ".modal-results").is_displayed()

    #We then close the modal
    close_modal(driver)
    time.sleep(1)

    #And check that the modal is truly closed
    assert "active" not in driver.find_element(By.ID, "quiz-overlay").get_attribute("class")

#We then test the full flow for a todo quiz card
def test_todo_quiz_full_flow(driver):
    login_user(driver)
    go_to_quizzes(driver)

    #We wait until a quiz card loads into the to-do section
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#todo-list .quiz-card"))
    )

    #We look for the time availability quiz card as charlie hasnt done it yet
    todo_cards = driver.find_elements(By.CSS_SELECTOR, "#todo-list .quiz-card")
    time_availability_card = next(
        card for card in todo_cards
        if "Time Availability" in card.find_element(By.CSS_SELECTOR, ".quiz-card-name").text
    )

    #We then open the selected quiz card
    time_availability_card.click()
    time.sleep(1)

    #We check that the intro modal slide is opened with the begin button
    assert driver.find_element(By.CSS_SELECTOR, ".modal-intro").is_displayed()
    begin_btn = driver.find_element(By.ID, "begin-btn")
    assert begin_btn.is_displayed()

    #We then click the begin button
    begin_btn.click()
    time.sleep(1)

    #And check that the question modal slide appears with the slider
    assert driver.find_element(By.CSS_SELECTOR, ".modal-question").is_displayed()
    assert driver.find_element(By.ID, "q-slider").is_displayed()

    #We call the helper function to answer all 10 questions
    answer_all_questions(driver)

    #We then confirm the results slide appears with exactly 2 keyword chips
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-results"))
    )
    assert driver.find_element(By.CSS_SELECTOR, ".modal-results").is_displayed()
    assert len(driver.find_elements(By.CSS_SELECTOR, ".keyword-chip")) == 2

#Finally we check that the sections update correctly after a quiz submission
def test_sections_update_after_submission(driver):
    login_user(driver)
    go_to_quizzes(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#todo-list .quiz-card"))
    )

    #We record the state of the progress bar and completed quiz card numbers to have as a comparison point
    initial_progress = driver.find_element(By.ID, "overall-progress-percent").text
    initial_completed_count = len(driver.find_elements(By.CSS_SELECTOR, "#completed-list .quiz-card"))

    #We find and click the time availability quiz card
    todo_cards = driver.find_elements(By.CSS_SELECTOR, "#todo-list .quiz-card")
    time_availability_card = next(
        card for card in todo_cards
        if "Time Availability" in card.find_element(By.CSS_SELECTOR, ".quiz-card-name").text
    )
    time_availability_card.click()
    time.sleep(1)

    #We complete the quiz by calling the helper function
    driver.find_element(By.ID, "begin-btn").click()
    time.sleep(1)
    answer_all_questions(driver)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-results"))
    )

    #We close the modal
    close_modal(driver)
    time.sleep(2)

    #We check the progress bar percentage has increased
    assert driver.find_element(By.ID, "overall-progress-percent").text != initial_progress

    #THen we check the completed section has one more card
    updated_completed_count = len(driver.find_elements(By.CSS_SELECTOR, "#completed-list .quiz-card"))
    assert updated_completed_count == initial_completed_count + 1

    #We check that there are no duplicate cards anywhere on the page
    all_cards = driver.find_elements(By.CSS_SELECTOR, ".quiz-card")
    card_names = [c.find_element(By.CSS_SELECTOR, ".quiz-card-name").text for c in all_cards]
    assert len(card_names) == len(set(card_names))