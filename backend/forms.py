"""
Forms with CSRF Protection and Input Validation
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from backend.models import User
from datetime import datetime

class LoginForm(FlaskForm):
    """Secure Login Form with CSRF Protection"""
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=80, message="Username must be between 3 and 80 characters")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=6, message="Password must be at least 6 characters")
        ]
    )
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """Secure Signup Form with CSRF Protection"""
    username = StringField(
        'Username (Email)',
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=80, message="Username must be between 3 and 80 characters"),
            Regexp(r'^[a-zA-Z0-9._@-]+$', message='Username must contain only letters, numbers, dots, hyphens, underscores, and @ symbol')
        ]
    )
    
    full_name = StringField(
        'Full Name',
        validators=[
            DataRequired(message="Full Name is required"),
            Length(min=2, max=80, message="Full Name must be between 2 and 80 characters")
        ]
    )
    
    qualification = StringField(
        'Qualification',
        validators=[
            DataRequired(message="Qualification is required"),
            Length(min=2, max=80, message="Qualification must be between 2 and 80 characters")
        ]
    )
    
    dob = DateField(
        'Date of Birth',
        validators=[DataRequired(message="Date of Birth is required")],
        format='%Y-%m-%d'
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required"),
            Length(min=8, message="Password must be at least 8 characters")
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Confirm Password is required"),
            EqualTo('password', message='Passwords must match')
        ]
    )
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists"""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

class SubjectForm(FlaskForm):
    """Form for Adding/Editing Subjects"""
    name = StringField(
        'Subject Name',
        validators=[
            DataRequired(message="Subject name is required"),
            Length(min=2, max=80, message="Subject name must be between 2 and 80 characters")
        ]
    )
    description = StringField(
        'Description',
        validators=[Length(max=200, message="Description must be less than 200 characters")]
    )
    submit = SubmitField('Save Subject')

class ChapterForm(FlaskForm):
    """Form for Adding/Editing Chapters"""
    name = StringField(
        'Chapter Name',
        validators=[
            DataRequired(message="Chapter name is required"),
            Length(min=2, max=80, message="Chapter name must be between 2 and 80 characters")
        ]
    )
    description = StringField(
        'Description',
        validators=[Length(max=200, message="Description must be less than 200 characters")]
    )
    submit = SubmitField('Save Chapter')

class QuizForm(FlaskForm):
    """Form for Adding/Editing Quizzes"""
    name = StringField(
        'Quiz Name',
        validators=[
            DataRequired(message="Quiz name is required"),
            Length(min=2, max=80, message="Quiz name must be between 2 and 80 characters")
        ]
    )
    date_of_quiz = DateField(
        'Quiz Date',
        validators=[DataRequired(message="Quiz date is required")],
        format='%Y-%m-%d'
    )
    time_duration = StringField(
        'Time Duration (HH:MM)',
        validators=[
            DataRequired(message="Time duration is required"),
            Regexp('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', message='Please use HH:MM format (00:00 to 23:59)')
        ]
    )
    remarks = StringField(
        'Remarks',
        validators=[Length(max=200, message="Remarks must be less than 200 characters")]
    )
    submit = SubmitField('Save Quiz')

class QuestionForm(FlaskForm):
    """Form for Adding/Editing Questions"""
    question_statement = StringField(
        'Question',
        validators=[
            DataRequired(message="Question is required"),
            Length(min=5, max=255, message="Question must be between 5 and 255 characters")
        ]
    )
    option1 = StringField(
        'Option 1',
        validators=[
            DataRequired(message="Option 1 is required"),
            Length(min=1, max=255, message="Option must be less than 255 characters")
        ]
    )
    option2 = StringField(
        'Option 2',
        validators=[
            DataRequired(message="Option 2 is required"),
            Length(min=1, max=255, message="Option must be less than 255 characters")
        ]
    )
    option3 = StringField(
        'Option 3',
        validators=[
            DataRequired(message="Option 3 is required"),
            Length(min=1, max=255, message="Option must be less than 255 characters")
        ]
    )
    option4 = StringField(
        'Option 4',
        validators=[
            DataRequired(message="Option 4 is required"),
            Length(min=1, max=255, message="Option must be less than 255 characters")
        ]
    )
    correct_answer = SelectField(
        'Correct Answer',
        choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')],
        validators=[DataRequired(message="Please select the correct answer")]
    )
    submit = SubmitField('Save Question')
