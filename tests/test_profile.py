import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


def test_login_success(driver):
    login(driver)

    assert "/dashboard" in driver.current_url


def test_profile_page_loads(driver):
    login(driver)

    driver.get(f"{BASE_URL}/profile")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "profile-name"))
    )

    assert "Profile" in driver.page_source
    assert driver.find_element(By.CLASS_NAME, "profile-name")
    assert driver.find_element(By.CLASS_NAME, "profile-username")
    assert driver.find_element(By.ID, "bioBox")


def test_edit_profile_button_redirects(driver):
    login(driver)

    driver.get(f"{BASE_URL}/profile")

    edit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Edit Profile"))
    )
    edit_button.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/edit_profile")
    )

    assert "/edit_profile" in driver.current_url


def test_edit_profile_page_loads(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "display_name"))
    )

    assert driver.find_element(By.NAME, "display_name")
    assert driver.find_element(By.NAME, "bio")
    assert driver.find_element(By.ID, "languageSearch")
    assert driver.find_element(By.ID, "unitInput")
    assert driver.find_element(By.ID, "languagesData")
    assert driver.find_element(By.ID, "unitsData")


def test_edit_profile_updates_basic_info(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    display_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "display_name"))
    )
    bio = driver.find_element(By.NAME, "bio")
    languages_data = driver.find_element(By.ID, "languagesData")
    units_data = driver.find_element(By.ID, "unitsData")

    display_name.clear()
    display_name.send_keys("User One")

    bio.clear()
    bio.send_keys("This is a Selenium test bio.")

    driver.execute_script("arguments[0].value = 'English';", languages_data)
    driver.execute_script("arguments[0].value = 'CITS3403';", units_data)

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "form.profile-card button[type='submit']"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    driver.execute_script("arguments[0].click();", save_button)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash-area"))
    )

    assert "Profile updated successfully" in driver.page_source or "/edit_profile" in driver.current_url


def test_invalid_unit_code_shows_error(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    unit_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "unitInput"))
    )

    unit_input.send_keys("invalidunit")
    unit_input.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "flash-area"), "Invalid unit code")
    )

    assert "Invalid unit code" in driver.page_source


def test_account_settings_page_loads(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "accountSettingsForm"))
    )

    assert driver.find_element(By.NAME, "email")
    assert driver.find_element(By.NAME, "new_password")
    assert driver.find_element(By.NAME, "confirm_new_password")
    assert driver.find_element(By.ID, "openPasswordPopup")
    assert driver.find_element(By.ID, "passwordPopup")


def test_account_settings_password_popup_opens(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "openPasswordPopup"))
    )
    save_button.click()

    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwordPopup"))
    )

    assert "show" in popup.get_attribute("class")


def test_account_settings_password_mismatch_alert(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    new_password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "new_password"))
    )
    confirm_password = driver.find_element(By.NAME, "confirm_new_password")

    new_password.send_keys("newpass123")
    confirm_password.send_keys("different123")

    driver.find_element(By.ID, "openPasswordPopup").click()

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert "do not match" in alert.text
    alert.accept()


def test_account_settings_requires_current_password(driver):
    login(driver)

    driver.get(f"{BASE_URL}/account_settings")

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email_input.send_keys("user1@student.uwa.edu.au")

    driver.find_element(By.ID, "openPasswordPopup").click()

    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwordPopup"))
    )

    assert "show" in popup.get_attribute("class")

    driver.find_element(By.ID, "confirmSubmit").click()

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert "Please enter your current password" in alert.text
    alert.accept()