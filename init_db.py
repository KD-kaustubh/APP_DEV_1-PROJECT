"""
Database initialization script
Creates fresh database with test credentials
"""

from app import app, db
from backend.models import User, Subject, Chapter
from datetime import datetime

def init_db():
    """Initialize database with tables and test data"""
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Create test admin user
        admin = User(
            username='admin@gmail.com',
            full_name='Admin User',
            qualification='Administrator',
            dob=datetime(2000, 1, 1).date(),
            role=0  # Admin role
        )
        admin.set_password('Admin123')  # Hash the password
        
        # Create test student user
        student = User(
            username='student@gmail.com',
            full_name='Student User',
            qualification='B.Tech',
            dob=datetime(2002, 5, 15).date(),
            role=1  # Student role
        )
        student.set_password('Student123')  # Hash the password
        
        # Add users to database
        db.session.add(admin)
        db.session.add(student)
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print("\n📝 Test Credentials:")
        print("─" * 50)
        print("Admin Login:")
        print("  Username: admin@gmail.com")
        print("  Password: Admin123")
        print("\nStudent Login:")
        print("  Username: student@gmail.com")
        print("  Password: Student123")
        print("─" * 50)

if __name__ == '__main__':
    init_db()
