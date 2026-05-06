import pytest, os
from web import create_app, db
from werkzeug.security import generate_password_hash
from web.api.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

"""
////////////////////////////////////////////////////////////////////////////
//                                                                          //
//  UNIT TEST FIXTURES                                                      //
//                                                                          //
/////////////////////////////////////////////////////////////////////////////
"""
@pytest.fixture
def app():
    # TESTING MODE CONFIG
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        
        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

"""
/////////////////////////////////////////////////////////////////////////////
//                                                                          //
//  HELPER FUNCTIONS                                                        //
//                                                                          //
/////////////////////////////////////////////////////////////////////////////
"""
@pytest.fixture
def runner(app):
    #Creates a CLI runner.
    return app.test_cli_runner()

def create_test_user(
    username="testuser",
    displayname="Test User",
    email="123456@student.uwa.edu.au",
    password="Password123",
    languages="English",
    studyunits="CITS3403"
):

    user = User(
        username=username,
        displayname=displayname,
        email=email,
        password=generate_password_hash(password),
        languages=languages,
        studyunits=studyunits
    )

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def test_user(app):
    """
    Pytest fixture that creates one default test user.
    """
    with app.app_context():
        return create_test_user()


@pytest.fixture
def logged_in_client(client, app):
    with app.app_context():
        user = create_test_user()

    with client.session_transaction() as session:
        session["user"] = user.username

    return client

"""
////////////////////////////////////////////////////////////////////////////
//                                                                         //
//  SELENIUM DRIVER FIXTURE                                                //
//                                                                         //
/////////////////////////////////////////////////////////////////////////////
"""

"""
    Creates a Selenium browser driver.

    Default browser: Chrome

    Run with different browsers:

        BROWSER=chrome pytest tests/selenium/test_login_ui.py
        BROWSER=firefox pytest tests/selenium/test_login_ui.py
        BROWSER=edge pytest tests/selenium/test_login_ui.py
        BROWSER=safari pytest tests/selenium/test_login_ui.py

    Safari only works on macOS.
    """
@pytest.fixture
def driver():
    browser = os.getenv("BROWSER", "chrome").lower()

    if browser == "firefox":
        options = FirefoxOptions()

        # Use this if do NOT want the browser window to open
        # options.add_argument("--headless")

        # Only use this if Selenium cannot find Firefox automatically
        # options.binary_location = "/usr/bin/firefox"

        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = EdgeOptions()

        # Use this if do NOT want the browser window to open
        # options.add_argument("--headless=new")

        # Only use this if Edge is installed inside WSL/Linux
        # options.binary_location = "/usr/bin/microsoft-edge"
        # options.binary_location = "/usr/bin/microsoft-edge-stable"

        options.add_argument("--window-size=1200,900")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Edge(options=options)

    elif browser == "safari":
        options = SafariOptions()

        # Safari only works on macOS.
        # Before using Safari, run this once on Mac:
        # safaridriver --enable
        #
        # Also enable:
        # Safari > Develop > Allow Remote Automation

        driver = webdriver.Safari(options=options)

    else:
        options = ChromeOptions()

        # Only use this if Selenium cannot find Chrome automatically
        options.binary_location = "/usr/bin/google-chrome"

        # Use this if do NOT want the browser window to open
        # options.add_argument("--headless=new")

        options.add_argument("--window-size=1200,900")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

    yield driver

    driver.quit()