from database import SessionLocal, engine
from models import User
import bcrypt

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_default_users():
    """Create default admin and reviewer users"""
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_admin = db.query(User).filter(User.username == "admin").first()
        existing_reviewer = db.query(User).filter(User.username == "reviewer").first()
        
        # Create Admin user
        if not existing_admin:
            admin_user = User(
                username="admin",
                email="admin@invoicehub.com",
                password=hash_password("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            print("✓ Admin user created successfully")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@invoicehub.com")
        else:
            print("✗ Admin user already exists")
        
        # Create Reviewer user
        if not existing_reviewer:
            reviewer_user = User(
                username="reviewer",
                email="reviewer@invoicehub.com",
                password=hash_password("reviewer123"),
                role="reviewer",
                is_active=True
            )
            db.add(reviewer_user)
            print("\n✓ Reviewer user created successfully")
            print("  Username: reviewer")
            print("  Password: reviewer123")
            print("  Email: reviewer@invoicehub.com")
        else:
            print("✗ Reviewer user already exists")
        
        # Commit changes
        db.commit()
        print("\n" + "="*50)
        print("Default users have been created successfully!")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"Error creating users: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating default users...")
    print("="*50)
    create_default_users()
