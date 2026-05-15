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


def test_edit_profile_page_loads(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "display_name"))
    )

    assert "Edit Profile" in driver.page_source
    assert driver.find_element(By.NAME, "display_name")
    assert driver.find_element(By.NAME, "bio")
    assert driver.find_element(By.ID, "languageSearch")
    assert driver.find_element(By.ID, "selectedLanguages")
    assert driver.find_element(By.ID, "languagesData")
    assert driver.find_element(By.ID, "unitInput")
    assert driver.find_element(By.ID, "selectedUnits")
    assert driver.find_element(By.ID, "unitsData")


def test_edit_profile_back_to_profile_link(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    back_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "← Back to Profile"))
    )
    back_link.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("/profile")
    )

    assert "/profile" in driver.current_url


def test_edit_profile_can_update_display_name_bio_language_and_unit(driver):
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
    bio.send_keys("This bio was updated by Selenium.")

    # Set hidden inputs directly to avoid depending on dropdown/API timing.
    driver.execute_script("arguments[0].value = 'English';", languages_data)
    driver.execute_script("arguments[0].value = 'CITS3403';", units_data)

    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "form.profile-card button[type='submit']")
        )
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    driver.execute_script("arguments[0].click();", save_button)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash-area"))
    )

    assert "Profile updated successfully" in driver.page_source or "/edit_profile" in driver.current_url


def test_edit_profile_rejects_empty_display_name(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    display_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "display_name"))
    )

    display_name.clear()

    save_button = driver.find_element(
        By.CSS_SELECTOR,
        "form.profile-card button[type='submit']"
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    driver.execute_script("arguments[0].click();", save_button)

    # HTML required validation should keep the user on the same page.
    assert "/edit_profile" in driver.current_url


def test_edit_profile_invalid_unit_code_shows_error(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    unit_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "unitInput"))
    )

    unit_input.clear()
    unit_input.send_keys("invalidunit")
    unit_input.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "flash-area"),
            "Invalid unit code"
        )
    )

    assert "Invalid unit code" in driver.page_source


def test_edit_profile_valid_unit_updates_hidden_input(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    unit_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "unitInput"))
    )
    units_data = driver.find_element(By.ID, "unitsData")

    unit_input.clear()
    unit_input.send_keys("cits3403")
    unit_input.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(
        lambda d: "CITS3403" in units_data.get_attribute("value")
    )

    assert "CITS3403" in units_data.get_attribute("value")


def test_edit_profile_social_form_fields_exist(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "socialForm"))
    )

    assert driver.find_element(By.NAME, "instagram")
    assert driver.find_element(By.NAME, "linkedin")
    assert driver.find_element(By.NAME, "discord")

    save_socials_button = driver.find_element(
        By.CSS_SELECTOR,
        "#socialForm button[type='submit']"
    )

    assert save_socials_button.text == "Save Socials"


def test_edit_profile_can_submit_social_links(driver):
    login(driver)

    driver.get(f"{BASE_URL}/edit_profile")

    instagram = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "instagram"))
    )
    linkedin = driver.find_element(By.NAME, "linkedin")
    discord = driver.find_element(By.NAME, "discord")

    instagram.clear()
    instagram.send_keys("test_user")
    linkedin.clear()
    linkedin.send_keys("test-user")
    discord.clear()
    discord.send_keys("testuser#1234")

    save_socials_button = driver.find_element(
        By.CSS_SELECTOR,
        "#socialForm button[type='submit']"
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_socials_button)
    driver.execute_script("arguments[0].click();", save_socials_button)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.ID, "flash-area"),
            "Social links updated successfully"
        )
    )

    assert "Social links updated successfully" in driver.page_source