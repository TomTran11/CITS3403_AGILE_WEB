"""
This tests the dashboard's ui which displays after loggin in
    1. Dashboard loads after login
    2. Greeting shows charlie's display name
    3. Search bar is visible and functional
    4. Match cards appear in the carousel
    5. View more link goes to matches page
    6. Heart button toggles liked state
    7. Clicking a match card navigates to their profile
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#This is a helper function just to sign in our fake user from the database
def login_user(driver, base_url, username="charlie", password="password"):
    driver.get(f"{base_url}/auth/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "loginForm"))
    )
    login_form = driver.find_element(By.ID, "loginForm")
    login_form.find_element(By.NAME, "username").send_keys(username)
    login_form.find_element(By.NAME, "password").send_keys(password)
    login_form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)

#THis tests that we are on the dashboard page
def test_dashboard_loads_after_login(driver, base_url):
    #We call the helper function to login
    login_user(driver, base_url)

    #We check were on the right page
    assert "/dashboard" in driver.current_url

    #And we also check that the content is visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-content"))
    )
    assert driver.find_element(By.CSS_SELECTOR, ".dashboard-content").is_displayed()

#We confirm that the greeting card has addresses the correct logged in user
def test_dashboard_shows_greeting(driver, base_url):
    #We call the helper function to login
    login_user(driver, base_url)

    greeting = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dashboard-greeting"))
    )
    assert "charlie" in greeting.text.lower()

#This tests that the search bar in the dashboard page is present
def test_dashboard_search_bar_visible(driver, base_url):
    #We call the helper function to login
    login_user(driver, base_url)

    #We check the search bar and also the search button
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-bar"))
    )
    assert search_bar.is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, ".search-btn").is_displayed()

#This function tests the searching ability of the search bar
def test_dashboard_search_navigates_to_results(driver, base_url):
    #We call the helper function to login
    login_user(driver, base_url)

    #We type the search into the search bar and click the button
    search_bar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-bar"))
    )
    search_bar.send_keys("alex")
    driver.find_element(By.CSS_SELECTOR, ".search-btn").click()

    #We finally confirm that the search was successful
    WebDriverWait(driver, 10).until(EC.url_contains("/search"))
    assert "/search" in driver.current_url
    assert "alex" in driver.current_url

#This tests the dashboards matched cards for the logged in user
def test_dashboard_match_cards_appear(driver, base_url):
    #We call the helper function to login
    login_user(driver, base_url)

    #We check the carousel and that the matching cards are visible
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "dashRecommendedCarousel"))
    )
    assert driver.find_element(By.ID, "dashRecommendedCarousel").is_displayed()

    #We check at least 1 card is visible
    cards = driver.find_elements(By.CSS_SELECTOR, ".user-card")
    assert len(cards) > 0

#This tests the view more button that is under the search bar
def test_dashboard_view_more_link(driver, base_url):
    # We call the helper function to login
    login_user(driver, base_url)

    # We then check that the view more link is visible and click it
    view_more = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".view-more-link"))
    )
    assert view_more.is_displayed()
    view_more.click()

    #We then confirm that we were redirect properly
    WebDriverWait(driver, 10).until(EC.url_contains("/matches"))
    assert "/matches" in driver.current_url

#This tests the heart button toggle on the page
def test_dashboard_heart_button_toggles(driver, base_url):
    #We call the helper function to login
    login_user(driver, base_url)

    #We find the heart button
    heart_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".heart-btn"))
    )
    initial_state = heart_btn.dataset if hasattr(heart_btn, 'dataset') else heart_btn.get_attribute("data-liked")

    #We then click the heart
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", heart_btn)
    time.sleep(0.5)
    heart_btn.click()
    time.sleep(1)

    #And check if the state of the hard changed
    new_state = heart_btn.get_attribute("data-liked")
    assert new_state != initial_state

#This tests that clicking on a match card brings up their profile
def test_dashboard_match_card_navigates_to_profile(driver, base_url):
    #We call the helper function to login
    login_user(driver, base_url)

    #We find the first match card and click on it
    card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".user-card"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
    time.sleep(0.5)
    card.click()

    #We then check that we were redirect to their profile
    WebDriverWait(driver, 10).until(EC.url_contains("/view_user"))
    assert "/view_user" in driver.current_url