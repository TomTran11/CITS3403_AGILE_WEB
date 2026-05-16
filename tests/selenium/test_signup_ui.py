"""
Selenium UI tests for signup page

1. Signup page opens
2. Required fields exist
3. User can type into fields
4. Submit button exists
5. Invalid signup shows error / stays on signup page
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException


def test_signup_page_loads(driver, base_url):
    driver.get(f"{base_url}/auth/signup")

    signup_form = driver.find_element(By.TAG_NAME, "form")

    username_input = signup_form.find_element(By.NAME, "username")
    display_name_input = signup_form.find_element(By.NAME, "display_name")
    unit_input = signup_form.find_element(By.ID, "unitInput")
    language_input = signup_form.find_element(By.ID, "languageInput")
    password_input = signup_form.find_element(By.NAME, "password")
    confirm_password_input = signup_form.find_element(By.NAME, "confirm_password")
    email_input = signup_form.find_element(By.NAME, "email")
    submit_button = signup_form.find_element(By.CSS_SELECTOR, "button[type='submit']")

    assert username_input.is_displayed()
    assert display_name_input.is_displayed()
    assert unit_input.is_displayed()
    assert language_input.is_displayed()
    assert password_input.is_displayed()
    assert confirm_password_input.is_displayed()
    assert email_input.is_displayed()
    assert submit_button.is_displayed()

    time.sleep(2)


def test_user_can_type_into_signup_form(driver, base_url):
    driver.get(f"{base_url}/auth/signup")
    time.sleep(2)

    signup_form = driver.find_element(By.TAG_NAME, "form")

    username_input = signup_form.find_element(By.NAME, "username")
    display_name_input = signup_form.find_element(By.NAME, "display_name")
    unit_input = signup_form.find_element(By.ID, "unitInput")
    language_input = signup_form.find_element(By.ID, "languageInput")
    selected_languages = signup_form.find_element(By.ID, "selectedLanguages")
    password_input = signup_form.find_element(By.NAME, "password")
    confirm_password_input = signup_form.find_element(By.NAME, "confirm_password")
    email_input = signup_form.find_element(By.NAME, "email")

    username_input.send_keys("newuser")
    display_name_input.send_keys("New User")

    unit_input.send_keys("CITS3403")
    unit_input.send_keys(Keys.ENTER)

    language_input.click()
    language_input.send_keys("English")

    english_option = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='dropdownList']//*[contains(normalize-space(), 'English')]")
        )
    )

    driver.execute_script("arguments[0].click();", english_option)

    WebDriverWait(driver, 5).until(
        lambda d: "English" in selected_languages.text
    )

    password_input.send_keys("Password123")
    confirm_password_input.send_keys("Password123")
    email_input.send_keys("12345678@student.uwa.edu.au")

    assert username_input.get_attribute("value") == "newuser"
    assert display_name_input.get_attribute("value") == "New User"
    assert "English" in selected_languages.text
    assert password_input.get_attribute("value") == "Password123"
    assert confirm_password_input.get_attribute("value") == "Password123"
    assert email_input.get_attribute("value") == "12345678@student.uwa.edu.au"

def test_invalid_signup_shows_error(driver, base_url):
    driver.get(f"{base_url}/auth/signup")
    time.sleep(1)

    signup_form = driver.find_element(By.TAG_NAME, "form")

    signup_form.find_element(By.NAME, "username").send_keys("baduser")
    signup_form.find_element(By.NAME, "display_name").send_keys("Bad User")

    unit_input = signup_form.find_element(By.ID, "unitInput")
    unit_input.send_keys("CITS3100")
    unit_input.send_keys(Keys.ENTER)

    signup_form.find_element(By.NAME, "password").send_keys("Password123")
    signup_form.find_element(By.NAME, "confirm_password").send_keys("Password123")
    signup_form.find_element(By.NAME, "email").send_keys("12345678@student.uwa.edu.au")

    submit_button = signup_form.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    # wait for and handle the alert
    alert_text = None
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
    except UnexpectedAlertPresentException:
        # alert was already present before we could switch
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

    # verify the alert had the expected message
    assert alert_text is not None
    assert "Please select at least one language" in alert_text

    # wait a bit for alert to fully dismiss and any remaining alerts to clear
    time.sleep(1)
    
    # dismiss any lingering alerts (failsafe)
    try:
        while True:
            alert = driver.switch_to.alert
            alert.accept()
    except Exception:
        pass

    time.sleep(1)
    assert "/auth/signup" in driver.current_url