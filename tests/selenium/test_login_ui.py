"""
1. Login page opens
2. Username/password fields exist
3. User can type into them
4. Submit button exists
5. Valid login redirects to dashboard
6. Invalid login shows error / stays on login page
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:60000"


def test_login_page_loads(driver):
    driver.get(f"{BASE_URL}/auth/login")

    login_form = driver.find_element(By.ID, "loginForm")
    username_input = login_form.find_element(By.NAME, "username")
    password_input = login_form.find_element(By.NAME, "password")
    submit_button = login_form.find_element(By.CSS_SELECTOR, "button[type='submit']")

    assert username_input.is_displayed()
    assert password_input.is_displayed()
    assert submit_button.is_displayed()
    time.sleep(5)


def test_user_can_type_into_login_form(driver):
    driver.get(f"{BASE_URL}/auth/login")
    time.sleep(2)

    login_form = driver.find_element(By.ID, "loginForm")
    username_input = login_form.find_element(By.NAME, "username")
    password_input = login_form.find_element(By.NAME, "password")
    time.sleep(1)

    username_input.send_keys("testuser")
    password_input.send_keys("Password123")
    time.sleep(1)

    assert username_input.get_attribute("value") == "testuser"
    assert password_input.get_attribute("value") == "Password123"


def test_invalid_login_shows_error(driver):
    driver.get(f"{BASE_URL}/auth/login")
    time.sleep(2)

    login_form = driver.find_element(By.ID, "loginForm")
    login_form.find_element(By.NAME, "username").send_keys("wronguser")
    login_form.find_element(By.NAME, "password").send_keys("wrongpassword")
    time.sleep(1)

    login_form.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    alert = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert"))
    )

    assert "/auth/login" in driver.current_url
    assert "invalid" in alert.text.lower()