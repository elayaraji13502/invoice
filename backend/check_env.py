import os
from dotenv import load_dotenv

# Load from backend directory
load_dotenv()

api_key = os.getenv("MINDEE_V2_API_KEY")
print(f"MINDEE_V2_API_KEY length: {len(api_key) if api_key else 0}")
print(f"First 20 chars: {api_key[:20] if api_key else 'None'}")
print(f"Full key: {api_key}")
