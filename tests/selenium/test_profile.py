"""
This tests the profile page UI.
    1. Profile page loads with name, username and bio elements
    2. Edit Profile button navigates to edit page
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Helper: login as a user from populate_DB.py (precondition, not a test itself)
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


def test_profile_page_loads(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/profile")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-name"))
    )

    assert "Profile" in driver.page_source
    assert driver.find_element(By.CLASS_NAME, "profile-name")
    assert driver.find_element(By.CLASS_NAME, "profile-username")
    assert driver.find_element(By.ID, "bioBox")


def test_edit_profile_button_redirects(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/profile")

    edit_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Edit Profile"))
    )

    # Use JS click to bypass any overlapping fixed elements (navbar, dropdowns)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", edit_button)
    driver.execute_script("arguments[0].click();", edit_button)

    WebDriverWait(driver, 10).until(EC.url_contains("/edit_profile"))

    assert "/edit_profile" in driver.current_url