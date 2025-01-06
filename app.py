from flask import Flask
from backend.models import db

# Declare app globally
app = Flask(__name__)

def setup_app():
    # Set the configuration for SQLAlchemy before initializing db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.sqlite3'  # Database URI
    db.init_app(app)  #flask app conn with db
    app.app_context().push()  # Direct access to other models
    app.debug = True
    print("Quiz Master app is started...")

# Calling setup function
setup_app()

# Import controllers after app setup
from backend.controllers import *

if __name__ == '__main__':
    app.run(debug=True)
