"""
Quick test script to run email ingestion
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from services.email_ingestion import connect_and_fetch

if __name__ == "__main__":
    print("Starting email ingestion test...")
    try:
        result = connect_and_fetch()
        print(f"\n✅ Ingestion completed successfully!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
