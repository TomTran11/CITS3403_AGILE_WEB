# CITS3403_AGILE_WEB

A Flask-based web application developed for the CITS3403 Agile Web Development unit.

---

##  Project Overview

This project is built using the Flask microframework and demonstrates:

- Backend development using Flask and Blueprints
- Secure user authentication system 
- Password reset via email using Flask-Mail 
- Dynamic frontend interactions using JavaScript (Fetch API) 
- Quiz based user profiling and personality keyword generation
- User matching system based on quiz answer similiarity between users
- Database populating for consistent testing across all environments
- Clean dependency management using virtual environments 
- Version control using Git and GitHub

---

##  Technologies Used

- Python 3
- Flask (Application Framework)
- Flask-SQLAlchemy (Database Management)
- Flask-WTF (CSRF Protection)
- Flask-Mail (Email Service)
- HTML, CSS, JavaScript
- Git & GitHub

---

##  Setup Instructions

Follow these steps to run the project locally.

---

### 1. Clone the Repository

```bash
git clone https://github.com/TomTran11/CITS3403_AGILE_WEB.git
cd CITS3403_AGILE_WEB
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate virtual Environment

#### Mac / Linux

```bash
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows

```bash
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration (.env)

Create a `.env` file inside the `web/` directory and add the following:

```env

SECRET_KEY=your-secret-key 
FLASK_DEBUG=true 
DATABASE_URL=sqlite:///app.db 

SESSION_COOKIE_SECURE=false 
SESSION_COOKIE_HTTPONLY=true 
SESSION_COOKIE_SAMESITE=Lax 
SESSION_PERMANENT_LIFETIME=120 

# Email Configuration (Flask-Mail) 
MAIL_SERVER=smtp.gmail.com 
MAIL_PORT=587 
MAIL_USE_TLS=true 
MAIL_USE_SSL=false 
MAIL_USERNAME=your_email@gmail.com 
MAIL_PASSWORD=your_app_password 
MAIL_SUPPRESS_SEND=false

```

### 6. Email Setup:
This project uses **Flask-Mail** to send password reset emails.

#### Steps to configure Gmail:

1. Go to your **Google Account → Security**
2. Enable **2-Step Verification**
3. Generate an **App Password**
4. Use the generated password in your `.env` file:

### 7. Database Setup:
This project uses a database populating script to populate test data via fake users.
It creates test users and inserts quiz results and keyword generation into the DB for actionable data such as the matching system.

python populating_DB.py

### 8. Run the application
```bash

flask --app web run

```

---

## Managing Dependencies

If new Python packages are installed during development, update the requirements.txt file so other team members can install the same dependencies.

```bash

pip freeze > requirements.txt

```

After updating the file, commit the changes:

```bash

git add requirements.txt
git commit -m "Update project dependencies"
git push

```

---

## Project Stucture

```
CITS3403_AGILE_WEB
├─ README.md
├─ populating_DB.py
├─ pytest.ini
├─ requirements.txt
├─ tests
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
└─ web
   ├─ __init__.py
   ├─ api
   │  ├─ __init__.py
   │  └─ models.py
   ├─ auth
   │  ├─ __init__.py
   │  ├─ routes.py
   │  └─ utils.py
   ├─ config.py
   ├─ data
   │  ├─ language_loader.py
   │  └─ languages.json
   ├─ main
   │  ├─ __init__.py
   │  └─ routes.py
   ├─ matching
   │  ├─ __init__.py
   │  ├─ routes.py
   │  └─ service.py
   ├─ quizzes
   │  ├─ __init__.py
   │  ├─ definitions.py
   │  ├─ routes.py
   │  └─ service.py
   ├─ services
   │  └─ mail_service.py
   ├─ static
   │  ├─ css
   │  │  ├─ about.css
   │  │  ├─ base.css
   │  │  ├─ dashboard.css
   │  │  ├─ login.css
   │  │  ├─ profile.css
   │  │  └─ signup.css
   │  └─ js
   │     ├─ base.js
   │     ├─ login.js
   │     ├─ quizzes.js
   │     ├─ reset_password.js
   │     ├─ signup1.js
   │     └─ signup2.js
   └─ templates
      ├─ auth
      │  ├─ about.html
      │  ├─ login.html
      │  ├─ reset_password.html
      │  └─ signup.html
      ├─ base.html
      ├─ main
      │  ├─ account_settings.html
      │  ├─ dashboard.html
      │  ├─ edit_profile.html
      │  ├─ landing_page.html
      │  └─ profile.html
      └─ quizzes
         └─ quizzes.html

```

## Database Migrations

This project uses Flask-Migrate (powered by Alembic) for database schema version control.

### Setup
Flask-Migrate is already initialised in this project. The `migrations/` folder contains all migration history.

### Applying Migrations
To apply all migrations and bring your database up to date:
flask --app web db upgrade

### Creating a New Migration
After making changes to models in `web/api/models.py`, generate a new migration:
flask --app web db migrate -m "Description of your change"
flask --app web db upgrade

### Rolling Back a Migration
To roll back to the previous migration:
flask --app web db downgrade

### Migration History
| Migration | Description |
|-----------|-------------|
| 179b2062e0f4 | Initial migration capturing all current models |

---

## References

- Umpirsky. (n.d.). Language List (ISO 639-1). 
Available at: https://github.com/umpirsky/language-list
Accessed: May 2026.

---

## Contributors

| Name | Student ID | GitHub |
|------|------------|--------|
| Tom Tran | 23459091 | [TomTran11](https://github.com/TomTran11) |
| Jiwon Song | 22965587 | [jiwon-07](https://github.com/jiwon-07) |
| Benjamin Gilmore | 23706738 | [bgilmore22](https://github.com/bgilmore22) |
| Eliza Hutchens | 24230437 | [arcococoa](https://github.com/arcococoa) |

---

## Notes
The .env file is not committed for security reasons.
Email functionality may take a few seconds depending on network conditions.
Password reset links are time-limited and single-use.