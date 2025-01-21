from flask import Flask
from backend.models import db
from dotenv import load_dotenv
import os

# Declare app globally
app = Flask(__name__)

def setup_app():
    # Load environment variables from .env file
    load_dotenv()

    # Set the configuration for SQLAlchemy and secret key from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///quizmaster.sqlite3')  # Database URI from .env
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')  # Secret key from .env
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize the SQLAlchemy object with the app
    db.init_app(app)

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
