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

def test_quizzes_page_loads_correctly(driver):
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