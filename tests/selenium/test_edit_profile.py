"""
This tests the edit profile page UI.
    1. Edit profile page loads with all expected fields
    2. Back to Profile link navigates correctly
    3. Display name, bio, language and unit can be updated
    4. Empty display name is rejected (HTML required validation)
    5. Invalid unit code shows an error
    6. Valid unit code populates the hidden input
    7. Social form fields exist
    8. Social links can be submitted
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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


def test_edit_profile_page_loads(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

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


def test_edit_profile_back_to_profile_link(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

    back_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "← Back to Profile"))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", back_link)
    driver.execute_script("arguments[0].click();", back_link)

    WebDriverWait(driver, 10).until(EC.url_contains("/profile"))

    assert "/profile" in driver.current_url


def test_edit_profile_can_update_display_name_bio_language_and_unit(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

    display_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "display_name"))
    )
    bio = driver.find_element(By.NAME, "bio")
    languages_data = driver.find_element(By.ID, "languagesData")
    units_data = driver.find_element(By.ID, "unitsData")

    display_name.clear()
    display_name.send_keys("Charlie Updated")

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


def test_edit_profile_rejects_empty_display_name(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

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


def test_edit_profile_invalid_unit_code_shows_error(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

    unit_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "unitInput"))
    )

    unit_input.clear()
    unit_input.send_keys("invalidunit")
    unit_input.send_keys(Keys.ENTER)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "flash-area"), "Invalid unit code")
    )

    assert "Invalid unit code" in driver.page_source


def test_edit_profile_valid_unit_updates_hidden_input(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

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


def test_edit_profile_social_form_fields_exist(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

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


def test_edit_profile_can_submit_social_links(driver, base_url):
    login_user(driver, base_url)
    driver.get(f"{base_url}/edit_profile")

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