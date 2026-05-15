import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:5000"
TEST_USERNAME = "user1"
TEST_PASSWORD = "1234"


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1400,1000")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def login(driver):
    driver.get(f"{BASE_URL}/auth/login")

    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = driver.find_element(By.NAME, "password")

    username_input.clear()
    username_input.send_keys(TEST_USERNAME)

    password_input.clear()
    password_input.send_keys(TEST_PASSWORD)

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )


def test_account_settings_page_loads(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

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


def test_account_settings_save_button_opens_password_popup(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "openPasswordPopup"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    driver.execute_script("arguments[0].click();", save_button)

    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwordPopup"))
    )

    assert "show" in popup.get_attribute("class")


def test_account_settings_cancel_button_closes_popup(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

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


def test_account_settings_requires_current_password(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_input.clear()
    email_input.send_keys("user1@student.uwa.edu.au")

    save_button = driver.find_element(By.ID, "openPasswordPopup")
    driver.execute_script("arguments[0].click();", save_button)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwordPopup"))
    )

    confirm_button = driver.find_element(By.ID, "confirmSubmit")
    driver.execute_script("arguments[0].click();", confirm_button)

    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    assert "Please enter your current password" in alert.text
    alert.accept()


def test_account_settings_password_mismatch_alert(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

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

    alert = WebDriverWait(driver, 10).until(
        EC.alert_is_present()
    )

    assert "do not match" in alert.text
    alert.accept()


def test_account_settings_current_password_hidden_input_updates(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_input.clear()
    email_input.send_keys("user1@student.uwa.edu.au")

    save_button = driver.find_element(By.ID, "openPasswordPopup")
    driver.execute_script("arguments[0].click();", save_button)

    current_password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "currentPasswordInput"))
    )

    current_password_input.clear()
    current_password_input.send_keys(TEST_PASSWORD)

    confirm_button = driver.find_element(By.ID, "confirmSubmit")
    driver.execute_script("arguments[0].click();", confirm_button)

    hidden_password = driver.find_element(By.ID, "currentPasswordHidden")

    assert hidden_password.get_attribute("value") == TEST_PASSWORD


def test_account_settings_rejects_invalid_email(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

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
    current_password_input.send_keys(TEST_PASSWORD)

    confirm_button = driver.find_element(By.ID, "confirmSubmit")
    driver.execute_script("arguments[0].click();", confirm_button)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "flash-alert"),
            "Email must be a valid UWA student email."
        )
    )

    assert "Email must be a valid UWA student email." in driver.page_source


def test_account_settings_no_changes_warning(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "openPasswordPopup"))
    )

    driver.execute_script("arguments[0].click();", save_button)

    current_password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "currentPasswordInput"))
    )
    current_password_input.clear()
    current_password_input.send_keys(TEST_PASSWORD)

    confirm_button = driver.find_element(By.ID, "confirmSubmit")
    driver.execute_script("arguments[0].click();", confirm_button)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "flash-alert"),
            "No changes were made."
        )
    )

    assert "No changes were made." in driver.page_source