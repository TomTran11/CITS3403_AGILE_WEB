"""
This tests the landing page UI.
    1. Landing page loads correctly
    2. Hero heading is visible
    3. Sign up and login buttons are present and link correctly
    4. Carousel is visible with slides
    5. How It Works section is visible with 3 steps
    6. Sign Up Now button in How It Works links to signup page
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#This is a helper function to help the tests run smoother by loggin the user in using the DB fake user charlie
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

#This tests if the landing page loads correctly upon opening
def test_landing_page_loads(driver, base_url):
    driver.get(f"{base_url}/")
    time.sleep(2)

    #We check that the page title is correct
    title = driver.find_element(By.TAG_NAME, "h1")
    assert title.is_displayed()
    assert "Find Your People" in title.text


def test_landing_page_signup_and_login_buttons(driver, base_url):
    driver.get(f"{base_url}/")
    time.sleep(2)

    #We then check that the sign up button exists and also links to signup page
    driver.find_element(By.LINK_TEXT, "Sign up").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/auth/signup"))
    assert "/auth/signup" in driver.current_url

    #We then check the other button login to see if it also exists and links to the login page
    driver.back()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Login").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/auth/login"))
    assert "/auth/login" in driver.current_url

#This tests the landing page's carousel
def test_landing_page_carousel_visible(driver, base_url):
    driver.get(f"{base_url}/")
    time.sleep(2)

    #We firstly check that the carousel is present
    carousel = driver.find_element(By.ID, "advertCarousel")
    assert carousel.is_displayed()

    #We then check to see if at least one of the carousel cards is active
    active_item = driver.find_element(By.CSS_SELECTOR, "#advertCarousel .carousel-item.active")
    assert active_item.is_displayed()

    #And we also check that there are 3 cards
    slides = driver.find_elements(By.CSS_SELECTOR, "#advertCarousel .carousel-item")
    assert len(slides) == 3

#This tests the bottom section of the landing page, the how to section
def test_landing_page_how_it_works_section(driver, base_url):
    driver.get(f"{base_url}/")
    time.sleep(2)

    #We first scroll down until we get to the section
    how_section = driver.find_element(By.CSS_SELECTOR, ".how-it-works")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", how_section)
    time.sleep(0.5)

    #We check for the sections title first
    assert driver.find_element(By.CSS_SELECTOR, ".how-title").is_displayed()
    assert "How It Works" in driver.find_element(By.CSS_SELECTOR, ".how-title").text

    #Then we confirm that all 3 steps of the how to section are there
    steps = driver.find_elements(By.CSS_SELECTOR, ".how-step")
    assert len(steps) == 3

    #And we also check that the step numbers are present
    numbers = driver.find_elements(By.CSS_SELECTOR, ".how-number")
    assert len(numbers) == 3
    assert numbers[0].text == "1"
    assert numbers[1].text == "2"
    assert numbers[2].text == "3"

#This tests the other features of the how to section
def test_how_it_works_cta(driver, base_url):
    driver.get(f"{base_url}/")
    time.sleep(2)

    # We scroll down until we reach the sign up now button
    cta_btn = driver.find_element(By.CSS_SELECTOR, ".how-cta-btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cta_btn)
    time.sleep(0.5)

    # We check the closing landing page text is there
    assert driver.find_element(By.CSS_SELECTOR, ".how-cta-text").is_displayed()
    assert "It really is that easy" in driver.find_element(By.CSS_SELECTOR, ".how-cta-text").text

    # We click the button and then confirm it navigates to signup page
    cta_btn.click()
    WebDriverWait(driver, 10).until(EC.url_contains("/auth/signup"))
    assert "/auth/signup" in driver.current_url

#This tests the landing page button and that it naviages to the right spot
def test_landing_page_signup_button_navigates(driver, base_url):
    driver.get(f"{base_url}/")
    time.sleep(2)

    #We click the button and check that it goes to the right spot
    driver.find_element(By.LINK_TEXT, "Sign up").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/auth/signup"))
    assert "/auth/signup" in driver.current_url