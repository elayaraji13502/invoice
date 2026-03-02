import psycopg2
import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
db_params = {
    'host': os.getenv("DB_HOST", "localhost"),
    'database': os.getenv("DB_NAME", "invoice"),
    'user': os.getenv("DB_USER", "postgres"),
    'password': os.getenv("DB_PASSWORD", "postgres123"),
    'port': os.getenv("DB_PORT", "5432")
}

def hash_password_bcrypt(password: str) -> str:
    """Hash a password using bcrypt (Python way)"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    print("Connected to PostgreSQL database successfully!")
    print("="*60)
    
    # First, delete all existing users
    cursor.execute("DELETE FROM users;")
    print("✅ Cleared existing users")
    
    # Create admin user with proper bcrypt hash
    admin_password = hash_password_bcrypt('admin123')
    cursor.execute("""
        INSERT INTO users (username, email, password, role, is_active)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, username, email, role;
    """, ('admin', 'admin@invoicehub.com', admin_password, 'admin', True))
    
    admin = cursor.fetchone()
    print(f"\n✅ Admin user created (ID: {admin[0]})")
    
    # Create reviewer user with proper bcrypt hash
    reviewer_password = hash_password_bcrypt('reviewer123')
    cursor.execute("""
        INSERT INTO users (username, email, password, role, is_active)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, username, email, role;
    """, ('reviewer', 'reviewer@invoicehub.com', reviewer_password, 'reviewer', True))
    
    reviewer = cursor.fetchone()
    print(f"✅ Reviewer user created (ID: {reviewer[0]})")
    
    # Commit changes
    conn.commit()
    
    # Verify the users
    cursor.execute("SELECT id, username, email, role, password FROM users ORDER BY id;")
    users = cursor.fetchall()
    
    print("\n" + "="*60)
    print("📋 CREATED USERS:")
    print("="*60)
    
    for user in users:
        user_id, username, email, role, password = user
        print(f"\nID: {user_id}")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Role: {role}")
        print(f"Password Hash: {password[:40]}...")
        print(f"Hash Type: bcrypt ✅")
    
    print("\n" + "="*60)
    print("🔑 VALID LOGIN CREDENTIALS:")
    print("="*60)
    print("\n👤 Admin Login:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n👤 Reviewer Login:")
    print("   Username: reviewer")
    print("   Password: reviewer123")
    print("\n" + "="*60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
