# Quiz Master - Professional Quiz Platform

A modern, secure, and feature-rich web-based quizzing platform built with Flask. Quiz Master enables educators to create and manage quizzes while allowing students to take assessments and track their performance.

##  Features

###  Security Features
- **Password Hashing**: BCrypt encryption for secure password storage
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms
- **Session Management**: Secure HTTPOnly cookies with 1-hour timeout
- **Rate Limiting**: 200 requests/day, 50 requests/hour per user
- **Form Validation**: Comprehensive input validation with WTForms
- **Role-Based Access**: Admin and Student role management

###  Admin Features
- Create and manage subjects
- Add chapters under subjects
- Create quizzes with date and time scheduling
- Add questions with multiple choice options
- Edit and delete subjects, chapters, and quizzes
- View user performance summaries
- Search functionality for subjects and chapters
- Admin dashboard with complete overview

###  Student Features
- Browse available quizzes by subject and chapter
- Take quizzes with time tracking
- View scores and performance history
- Track progress across multiple quizzes
- Search for specific quizzes
- View summary statistics
- Secure access to personal dashboard

##  Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd APP_DEV_1-PROJECT
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python init_db.py
```

**Test Credentials:**
- Admin: `admin@gmail.com` / `Admin123`
- Student: `student@gmail.com` / `Student123`

### 5. Run Application
```bash
python app.py
```

Access at: **http://127.0.0.1:5000**

##  Usage Guide

### For Students
1. **Sign Up**: Create account with email, name, qualification, DOB, and password
2. **Login**: Use credentials to access dashboard
3. **Browse Quizzes**: View available quizzes organized by subject and chapter
4. **Take Quiz**: Click "Start Quiz" to begin assessment
5. **Submit Answers**: Answer all questions and submit
6. **View Scores**: Check results and track performance in "My Scores" section
7. **View Summary**: See overall statistics and progress

### For Admins
1. **Login**: Use admin credentials
2. **Manage Subjects**: Create, edit, delete subjects
3. **Manage Chapters**: Add chapters to subjects
4. **Create Quizzes**: Create quizzes under chapters with dates and durations
5. **Add Questions**: Add multiple-choice questions to quizzes
6. **View Summary**: Check student performance and quiz statistics
7. **Search**: Find subjects, chapters, or quizzes quickly
