"""
Startup script to initialize the application:
1. Run email ingestion to fetch and process new invoices
2. Start both backend and frontend servers
"""
import subprocess
import time
import sys
import os

def run_email_ingestion():
    """Run email ingestion to fetch new invoices"""
    print("\n" + "="*60)
    print("🔍 STEP 1: Checking for new invoices from email...")
    print("="*60)
    
    try:
        result = subprocess.run(
            [sys.executable, "backend/services/email_ingestion.py"],
            cwd=os.getcwd(),
            capture_output=False,
            text=True
        )
        if result.returncode != 0:
            print("⚠️  Email ingestion had some issues, but continuing...")
    except FileNotFoundError:
        print("⚠️  Could not run email ingestion directly, will run via API instead...")
        return False
    
    return True

def start_servers():
    """Start backend and frontend servers using npm"""
    print("\n" + "="*60)
    print("🚀 STEP 2: Starting backend and frontend servers...")
    print("="*60 + "\n")
    
    try:
        result = subprocess.run(
            ["npm", "run", "start:all"],
            cwd=os.getcwd()
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ npm not found. Make sure Node.js is installed.")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("📦 INVOICE HUB - STARTUP SCRIPT")
    print("="*60)
    
    # Step 1: Run email ingestion
    run_email_ingestion()
    
    # Brief pause
    print("\nWaiting 2 seconds before starting servers...")
    time.sleep(2)
    
    # Step 2: Start servers
    success = start_servers()
    
    sys.exit(0 if success else 1)
