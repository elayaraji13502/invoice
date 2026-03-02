"""
Migration script to add reviewed_by and reviewed_at columns to invoices table
"""
import os
from dotenv import load_dotenv
from sqlalchemy import text, create_engine

# Load environment variables
load_dotenv()

# Get database credentials
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "invoice")

# Create connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

print("Adding reviewed_by and reviewed_at columns to invoices table...")

try:
    with engine.connect() as connection:
        # Check if columns exist before adding them
        result = connection.execute(
            text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='invoices' AND column_name='reviewed_by'
            """)
        )
        
        if not result.fetchone():
            print("Adding reviewed_by column...")
            connection.execute(text("""
            ALTER TABLE invoices ADD COLUMN reviewed_by VARCHAR(255) NULL;
            """))
            print("✓ reviewed_by column added")
        else:
            print("✓ reviewed_by column already exists")
        
        # Check for reviewed_at column
        result = connection.execute(
            text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='invoices' AND column_name='reviewed_at'
            """)
        )
        
        if not result.fetchone():
            print("Adding reviewed_at column...")
            connection.execute(text("""
            ALTER TABLE invoices ADD COLUMN reviewed_at TIMESTAMP NULL;
            """))
            print("✓ reviewed_at column added")
        else:
            print("✓ reviewed_at column already exists")
        
        connection.commit()
        print("\nMigration completed successfully!")
        
except Exception as e:
    print(f"Error during migration: {e}")
    raise
