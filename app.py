from flask import Flask
from backend.models import db, bcrypt, User
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
from sqlalchemy import inspect
from datetime import datetime

# Declare app globally
app = Flask(__name__)

# Initialize rate limiter for brute force protection
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

def setup_app():
    # Load environment variables from .env file
    load_dotenv()

    # Set the configuration for SQLAlchemy and secret key from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///quizmaster.sqlite3')  # Database URI from .env
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key_change_this')  # Secret key from .env
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    
    # Security configurations
    flask_env = os.getenv('FLASK_ENV', 'development').lower()
    app.config['SESSION_COOKIE_SECURE'] = flask_env == 'production'  # HTTPS only in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout
    app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit on CSRF tokens

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)

    # Ensure tables exist in environments without a pre-populated database
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('user'):
            db.create_all()
            print("Database tables created on startup.")

        # Seed default admin and student if no users exist
        if User.query.count() == 0:
            admin = User(
                username='admin@gmail.com',
                full_name='Admin User',
                qualification='Administrator',
                dob=datetime(2000, 1, 1).date(),
                role=0
            )
            admin.set_password('Admin123')

            student = User(
                username='student@gmail.com',
                full_name='Student User',
                qualification='B.Tech',
                dob=datetime(2002, 5, 15).date(),
                role=1
            )
            student.set_password('Student123')

            db.session.add(admin)
            db.session.add(student)
            db.session.commit()
            print("Seeded default admin and student users.")

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Direct access to other models
    app.app_context().push()

    # Enable debug mode for development
    app.debug = True
    print("Quiz Master app is started...")

# Calling setup function
setup_app()

# Import controllers (routes) after app setup to avoid circular imports
from backend.controllers import *

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
