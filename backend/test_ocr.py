"""
Test OCR extraction with a sample invoice PDF content
"""
import os
from dotenv import load_dotenv
from services.email_ingestion import ocr_and_extract_data

load_dotenv()

# Create a simple test - try with a minimal PDF
print("Testing OCR extraction...")
print(f"API Key loaded: {len(os.getenv('MINDEE_V2_API_KEY', ''))} chars")
print(f"Model ID: {os.getenv('MINDEE_MODEL_ID')}")

# Download a sample invoice from Mindee's test files
import requests

sample_url = "https://mindee-api-staging.s3.amazonaws.com/temp/2021/08/invoice.pdf"

try:
    response = requests.get(sample_url, timeout=5)
    if response.status_code == 200:
        pdf_bytes = response.content
        print(f"Downloaded sample invoice: {len(pdf_bytes)} bytes")
        
        result = ocr_and_extract_data("sample_invoice.pdf", pdf_bytes)
        if result:
            print(f"✅ OCR Success!")
            print(f"  Vendor: {result.get('vendor_name')}")
            print(f"  Invoice #: {result.get('invoice_number')}")
            print(f"  Amount: ${result.get('amount')}")
        else:
            print("❌ OCR returned None")
    else:
        print(f"Failed to download sample: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
