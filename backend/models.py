#DATA modelS

from flask_sqlalchemy import SQLAlchemy
from datetime import time
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

'''
User is parent of Score
Subject is parent of Chapter
Chapter is parent of Quiz
Quiz is parent of Question and Score
'''

# User model
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Increased to 255 for bcrypt hash
    role = db.Column(db.Integer, default=1)  #roles 0 for Admin 1 for User
    full_name = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)  #dob
    is_active = db.Column(db.Boolean, default=True)
    
    # relations define here
    scores = db.relationship("Score", backref="user", lazy=True, cascade="all,delete")
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Verify password"""
        return bcrypt.check_password_hash(self.password, password)
    
    def get_id(self):
        """Override get_id for Flask-Login"""
        return str(self.id)

# Subject model
class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    
    # relations define here
    chapters = db.relationship("Chapter", backref="subject", lazy=True, cascade="all,delete")

# Chapter model
class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    
    # relations define here
    quizzes = db.relationship("Quiz", backref="chapter", lazy=True, cascade="all,delete")

# Quiz model
class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    name=db.Column(db.String(80), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(db.Time, nullable=False)  #time in hh:mm
    remarks = db.Column(db.String(200),nullable=False)
    
    # relations define here
    questions = db.relationship("Question", backref="quiz", lazy=True, cascade="all,delete")
    scores = db.relationship("Score", backref="quiz", lazy=True, cascade="all,delete")
    
# Question modal
class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    question_statement = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(80), nullable=False)

# Score modal
class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False)
    total_score = db.Column(db.Float, nullable=False)
