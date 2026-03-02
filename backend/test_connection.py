import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Common passwords to try
passwords_to_try = [
    os.getenv("DB_PASSWORD", "postgres123"),
    "postgres",
    "admin",
    "root",
    "postgres@123",
    "password",
    "12345",
    ""
]

DB_USER = os.getenv("DB_USER", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")  # Try connecting to default postgres database

print("Testing PostgreSQL connection with different passwords...")
print(f"Host: {DB_HOST}")
print(f"Port: {DB_PORT}")
print(f"User: {DB_USER}")
print()

connection_successful = False

for password in passwords_to_try:
    try:
        print(f"Trying password: {'(empty)' if password == '' else '***'}")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=password,
            database=DB_NAME
        )
        print(f"✓ SUCCESS! Connected with password: {password}")
        print(f"\nUpdate your .env file with:")
        print(f"DB_PASSWORD={password}")
        conn.close()
        connection_successful = True
        break
    except psycopg2.OperationalError as e:
        if "password authentication failed" in str(e):
            print("✗ Password incorrect")
        else:
            print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

if not connection_successful:
    print("\n" + "="*60)
    print("Could not connect with any common password.")
    print("\nPlease reset your PostgreSQL password:")
    print("1. Open pgAdmin 4")
    print("2. Right-click on 'PostgreSQL 18' -> Properties")
    print("3. Go to 'Connection' tab")
    print("4. Or use SQL: ALTER USER postgres PASSWORD 'postgres123';")
    print("\nOr run as Administrator:")
    print('psql -U postgres -c "ALTER USER postgres PASSWORD \'postgres123\';"')
    print("="*60)
