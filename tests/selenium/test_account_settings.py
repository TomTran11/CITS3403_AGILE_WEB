"""
This tests the account settings page UI.
    1. Account settings page loads with all form fields
    2. Save button opens the password confirmation popup
    3. Cancel button closes the popup
    4. Submission without current password shows an alert
    5. Mismatched new/confirm passwords show an alert
    6. Invalid (non-UWA) email is rejected
    7. Submitting with no changes shows a warning
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Helper: login as a user from populate_DB.py
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


def test_account_settings_page_loads(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/account_settings")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "accountSettingsForm"))
    )

    assert "Account Settings" in driver.page_source
    assert driver.find_element(By.ID, "accountSettingsForm")
    assert driver.find_element(By.NAME, "email")
    assert driver.find_element(By.NAME, "new_password")
    assert driver.find_element(By.NAME, "confirm_new_password")
    assert driver.find_element(By.NAME, "current_password")
    assert driver.find_element(By.ID, "openPasswordPopup")
    assert driver.find_element(By.ID, "passwordPopup")


def test_account_settings_save_button_opens_password_popup(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/account_settings")

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "openPasswordPopup"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    driver.execute_script("arguments[0].click();", save_button)

    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwordPopup"))
    )

    assert "show" in popup.get_attribute("class")


def test_account_settings_cancel_button_closes_popup(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/account_settings")

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "openPasswordPopup"))
    )

    driver.execute_script("arguments[0].click();", save_button)

    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwordPopup"))
    )

    assert "show" in popup.get_attribute("class")

    cancel_button = driver.find_element(By.ID, "cancelPopup")
    driver.execute_script("arguments[0].click();", cancel_button)

    WebDriverWait(driver, 10).until(
        lambda d: "show" not in popup.get_attribute("class")
    )

    assert "show" not in popup.get_attribute("class")


def test_account_settings_requires_current_password(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/account_settings")

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_input.clear()
    email_input.send_keys("charlie@student.uwa.edu.au")

    save_button = driver.find_element(By.ID, "openPasswordPopup")
    driver.execute_script("arguments[0].click();", save_button)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwordPopup"))
    )

    confirm_button = driver.find_element(By.ID, "confirmSubmit")
    driver.execute_script("arguments[0].click();", confirm_button)

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())

    assert "Please enter your current password" in alert.text
    alert.accept()


def test_account_settings_password_mismatch_alert(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/account_settings")

    new_password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "new_password"))
    )
    confirm_password = driver.find_element(By.NAME, "confirm_new_password")

    new_password.clear()
    new_password.send_keys("newpass123")

    confirm_password.clear()
    confirm_password.send_keys("different123")

    save_button = driver.find_element(By.ID, "openPasswordPopup")
    driver.execute_script("arguments[0].click();", save_button)

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())

    assert "do not match" in alert.text
    alert.accept()


def test_account_settings_rejects_invalid_email(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/account_settings")

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_input.clear()
    email_input.send_keys("invalid-email@gmail.com")

    save_button = driver.find_element(By.ID, "openPasswordPopup")
    driver.execute_script("arguments[0].click();", save_button)

    current_password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "currentPasswordInput"))
    )
    current_password_input.clear()
    current_password_input.send_keys("password")

    confirm_button = driver.find_element(By.ID, "confirmSubmit")
    driver.execute_script("arguments[0].click();", confirm_button)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "flash-alert"),
            "Email must be a valid UWA student email."
        )
    )

    assert "Email must be a valid UWA student email." in driver.page_source


def test_account_settings_no_changes_warning(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/account_settings")

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "openPasswordPopup"))
    )

    driver.execute_script("arguments[0].click();", save_button)

    current_password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "currentPasswordInput"))
    )
    current_password_input.clear()
    current_password_input.send_keys("password")

    confirm_button = driver.find_element(By.ID, "confirmSubmit")
    driver.execute_script("arguments[0].click();", confirm_button)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "flash-alert"),
            "No changes were made."
        )
    )

    assert "No changes were made." in driver.page_source