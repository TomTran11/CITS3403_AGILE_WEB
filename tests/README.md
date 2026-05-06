# Testing Guide

This folder contains the automated tests for the Flask web application.

The tests are separated into two main groups:

1. **Backend tests**  
   These use `pytest` and Flask’s test client.

2. **Selenium UI tests**  
   These use Selenium to open a real browser and test the application like a user.

---

## Test Structure

```text
tests
│  ├─ README.md
│  ├─ backend
│  │  ├─ test_about.py
│  │  ├─ test_forgot_&_reset_pass.py
│  │  ├─ test_landing_page.py
│  │  ├─ test_login.py
│  │  ├─ test_protected_routes.py
│  │  └─ test_signup.py
│  ├─ conftest.py
│  └─ selenium
│     ├─ test_login_ui.py
│     └─ test_signup_ui.py
```

---

## Requirements

Make sure the virtual environment is activated before running tests.

```bash

source venv/bin/activate

```

Install the required packages:

```bash

pip install -r requirements.txt

```

---

## Backend Tests

Backend tests use Flask’s test client.

They are used to test:

- Route responses
- Login logic
- Signup logic
- Forgot password logic
- Protected routes
- Database behaviour
- JSON responses

Backend tests do not open a browser.

1. Run all backend tests:

```bash

pytest tests/backend

```

2. Run a single backend test file:

```bash

pytest tests/backend/test_login.py

```

3. Run all tests:

```bash

pytest

```

---

## Selenium UI Tests

Selenium tests open a real browser and test the website from a user’s perspective.

They are used to test:

- Page loading
- Visible form fields
- Typing into inputs
- Clicking buttons
- Redirects
- Flash/error messages
- JavaScript-driven UI behaviour

Selenium tests are slower than backend tests because they use a real browser.

1. Before running Selenium tests, start the Flask server in one terminal:

```bash

flask --app web run

```

2. Open another terminal and run:

```bash

pytest tests/selenium/test_login_ui.py

```

### Browser Selection
The Selenium fixture supports different browsers using the BROWSER environment variable.

Chrome is the default browser.

1. Run with Chrome:

```bash

BROWSER=chrome pytest selenium/test_login_ui.py

```

2. Run with Firefox:

```bash

BROWSER=firefox pytest selenium/test_login_ui.py

```

3. Run with Edge:

```bash

BROWSER=edge pytest selenium/test_login_ui.py

```

4. Run with Safari(Safari only works on macOS):

```bash

BROWSER=safari pytest selenium/test_login_ui.py

```

---

## FIXTURES
| Fixture | Purpose |
|---|---|
| `app` | Creates the Flask app in testing mode |
| `client` | Creates a Flask test client for backend route tests |
| `test_user` | Creates one default test user in the test database |
| `logged_in_client` | Creates a test client with a logged-in session |
| `driver` | Creates a Selenium browser driver |
