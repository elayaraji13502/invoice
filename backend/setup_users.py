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
    
    # Check existing users
    cursor.execute("SELECT id, username, email, role, password FROM users;")
    users = cursor.fetchall()
    
    if not users:
        print("\n❌ No users found in database!")
        print("\nCreating admin and reviewer users...")
        
        # Create users with bcrypt hashed passwords
        admin_password = hash_password_bcrypt('admin123')
        reviewer_password = hash_password_bcrypt('reviewer123')
        
        cursor.execute("""
            INSERT INTO users (username, email, password, role, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """, ('admin', 'admin@invoicehub.com', admin_password, 'admin', True))
        
        cursor.execute("""
            INSERT INTO users (username, email, password, role, is_active)
            VALUES (%s, %s, %s, %s, %s)
        """, ('reviewer', 'reviewer@invoicehub.com', reviewer_password, 'reviewer', True))
        
        conn.commit()
        
        print("✅ Users created successfully!")
        print("\nAdmin Credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nReviewer Credentials:")
        print("  Username: reviewer")
        print("  Password: reviewer123")
        
    else:
        print("\n📋 Existing Users:")
        print("-"*60)
        for user in users:
            user_id, username, email, role, password = user
            print(f"\nID: {user_id}")
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Role: {role}")
            print(f"Password Hash: {password[:30]}...")
            
            # Check if password looks like bcrypt hash
            if password.startswith('$2b$') or password.startswith('$2a$') or password.startswith('$2y$'):
                print(f"✅ Password is properly hashed (bcrypt)")
            else:
                print(f"⚠️  Password format unclear - may need rehashing")
                
                # Rehash the password
                if username == 'admin':
                    new_hash = hash_password_bcrypt('admin123')
                    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_hash, username))
                    print(f"✅ Rehashed password for {username}")
                elif username == 'reviewer':
                    new_hash = hash_password_bcrypt('reviewer123')
                    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_hash, username))
                    print(f"✅ Rehashed password for {username}")
                
        conn.commit()
        
    print("\n" + "="*60)
    print("\n🔑 VALID LOGIN CREDENTIALS:")
    print("="*60)
    print("\nAdmin Login:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nReviewer Login:")
    print("  Username: reviewer")
    print("  Password: reviewer123")
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
