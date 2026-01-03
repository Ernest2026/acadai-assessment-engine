# Acad AI - Assessment Engine Backend

A modular and secure assessment engine built with **Django** and **Django REST Framework**. This project manages academic courses, exams, and automated grading through a keyword-matching algorithm.

## 🚀 Features

- **Custom User Model**: Extended `AbstractUser` for flexible student/admin authentication.
- **Relational Schema**: Clean database design linking Courses -> Exams -> Questions -> Submissions -> Answers.
- **Secure Submissions**: Endpoints protected by Token Authentication, ensuring students only access their own data.
- **Automated Grading Service**: A custom logic layer in `utils.py` that evaluates student answers against expected answers using keyword density.
- **Optimized Performance**: Implements `select_related` and `prefetch_related` to minimize database hits.

---

## 🛠️ Setup Instructions

Follow these steps to get the project running locally.

### 1. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
Install all required packages using pip.
```bash
pip install -r requirements.txt
```

### 3. Database Setup
Generate and apply migrations to set up the database schema.
```bash
python manage.py makemigrations core assessment
python manage.py migrate
```
This will create all tables for users, courses, exams, questions, submissions, and answers.

### 4. Create a Superuser (Optional)
If you want access to the Django admin panel, create a superuser.
```bash
python manage.py createsuperuser
```
You’ll be prompted to provide a username, email, and password.

### 5. Run the Development Server
Start the local development server.
```bash
python manage.py runserver
```
The API will be available at: http://127.0.0.1:8000/

### Postman Documentation
https://www.postman.com/ernesto2026/workspace/acadai/collection/18762738-2b0a167f-a72c-41af-b0ff-c4a136d2d107?action=share&creator=18762738

### Database Design
https://dbdiagram.io/d/6954154639fa3db27bd5a05b

### 🧠 Automated Grading Mechanism

The grading logic is implemented in assessment/utils.py.

How grading works:

- The student’s answer and the question’s expected answer are retrieved.
- Both texts are normalized (lowercased and stripped of special characters).
- Keywords are compared to find overlaps.
- A score is calculated based on keyword matches relative to the question’s max_score.

This keeps grading predictable, explainable, and easy to adjust.