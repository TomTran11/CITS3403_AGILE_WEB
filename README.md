# CITS3403_AGILE_WEB

A Flask-based web application developed for the CITS3403 Agile Web Development unit.

---

##  Project Overview

This project is built using the Flask microframework and demonstrates:

- Backend development with Flask
- Clean dependency management using virtual environments
- Version control using Git and GitHub
- Professional project setup practices

---

##  Technologies Used

- Python 3
- Flask
- Virtual Environment (venv)
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

### 5. Run the application
```bash
flask run
```

---

## Project Stucture

```bash

CITS3403_AGILE_WEB
├── .env
├── .git
├── .gitignore
├── README.md
├── requirements.txt
├── venv
└── web
    ├── __init__.py
    └── routes.py
    
```
