import imaplib
import email
import datetime
import io
import os
import pickle
import time
from email.header import decode_header
from dotenv import load_dotenv
from mindee import ClientV2, InferenceParameters, BytesInput
from sqlalchemy.orm import Session
from models import Invoice, LineItem, EmailIngestionLog
from database import SessionLocal
import logging
from typing import List, Tuple, Dict

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================= CONFIGURATION =================

EMAIL_USER = os.getenv("EMAIL_USER", "invoice.project01@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "pend sdym nkzx hrzg")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
PROCESSED_LABEL = os.getenv("PROCESSED_LABEL", "Processed_Invoices")

# OCR Config
MINDEE_API_KEY = os.getenv("MINDEE_V2_API_KEY")
MINDEE_MODEL_ID = os.getenv("MINDEE_MODEL_ID", "1cd90980-2c6c-4d30-8952-af92c6db8786")

# Google Drive Config
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "1LoRbKdiCsO4UpC2ahXcjdS4O5Nz3-ua_")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = "token.pickle"
SCOPES = ["https://www.googleapis.com/auth/drive"]

# Invoice keywords
INVOICE_TERMS = [
    "invoice", "bill", "payment", "receipt", "total", "due",
    "order", "statement", "quote", "estimate", "contract",
    "subscription", "purchase", "transaction", "amount", "inv"
]

ALLOWED_EXTENSIONS = ('.pdf', '.jpg', '.jpeg', '.png', '.webp')

# ================= GOOGLE DRIVE AUTHENTICATION =================

def get_drive_service():
    """Authenticate and return Google Drive service"""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(f"❌ {CREDENTIALS_FILE} not found.")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)

# ================= OCR EXTRACTION =================

def ocr_and_extract_data(file_name: str, file_bytes: bytes) -> Dict:
    """Extract invoice data using Mindee OCR with retry logic"""
    max_retries = 3
    try:
        for attempt in range(max_retries):
            try:
                mindee_client = ClientV2(api_key=MINDEE_API_KEY)
                params = InferenceParameters(
                    model_id=MINDEE_MODEL_ID,
                    rag=None,
                    raw_text=None,
                    polygon=None,
                    confidence=None,
                )
                
                input_source = BytesInput(file_bytes, filename=file_name)
                response = mindee_client.enqueue_and_get_inference(input_source, params)
                fields = response.inference.result.fields
                break
            except Exception as inner_e:
                if attempt < max_retries - 1:
                    logger.warning(f"OCR attempt {attempt+1} failed, retrying in 3s: {str(inner_e)}")
                    time.sleep(3)
                else:
                    raise
        
        # Extract date with proper None handling
        date_value = None
        if "date" in fields and fields["date"].value:
            date_value = str(fields["date"].value)
        else:
            date_value = datetime.datetime.now().isoformat()
        
        data = {
            "invoice_number": fields.get("invoice_number", {}).value if "invoice_number" in fields else "N/A",
            "customer_name": fields.get("customer_name", {}).value if "customer_name" in fields else "N/A",
            "date": date_value,
            "vendor_name": fields.get("supplier_name", {}).value if "supplier_name" in fields else "N/A",
            "po_number": fields.get("po_number", {}).value if "po_number" in fields else "N/A",
            "amount": float(fields.get("total_amount", {}).value or 0) if "total_amount" in fields else 0.0,
            "tax": float(fields.get("total_tax", {}).value or 0) if "total_tax" in fields else 0.0,
        }
        
        line_items = []
        if "line_items" in fields and fields["line_items"].items:
            for item in fields["line_items"].items:
                sub = item.fields
                line_items.append({
                    "description": sub.get("description", {}).value if "description" in sub else "N/A",
                    "quantity": float(sub.get("quantity", {}).value or 0) if "quantity" in sub else 0,
                    "unit_price": float(sub.get("unit_price", {}).value or 0) if "unit_price" in sub else 0,
                    "total_price": float(sub.get("total_price", {}).value or 0) if "total_price" in sub else 0,
                })
        
        data["line_items"] = line_items
        data["total_amount"] = data["amount"] + data["tax"]
        
        return data
    except Exception as e:
        logger.error(f"OCR error for {file_name}: {str(e)}")
        return None

# ================= GOOGLE DRIVE UPLOAD =================

def upload_to_drive(file_bytes: bytes, filename: str) -> Tuple[str, str]:
    """Upload file to Google Drive"""
    try:
        drive_service = get_drive_service()
        media = MediaIoBaseUpload(
            io.BytesIO(file_bytes),
            mimetype="application/octet-stream",
            resumable=True
        )
        metadata = {"name": filename, "parents": [GOOGLE_DRIVE_FOLDER_ID]}
        
        uploaded = drive_service.files().create(
            body=metadata,
            media_body=media,
            fields="id, webViewLink"
        ).execute()
        
        return uploaded.get("id"), uploaded.get("webViewLink")
    except Exception as e:
        logger.error(f"Drive upload error for {filename}: {str(e)}")
        return None, None

# ================= DATABASE OPERATIONS =================

def save_invoice_to_db(
    ocr_data: Dict,
    drive_file_id: str,
    drive_link: str,
    email_subject: str,
    file_name: str,
    pdf_url: str = None
) -> int:
    """Save invoice and line items to database"""
    db = SessionLocal()
    try:
        # Create invoice
        invoice = Invoice(
            invoice_number=ocr_data.get("invoice_number", f"INV-{datetime.datetime.now().timestamp()}"),
            vendor_name=ocr_data.get("vendor_name", "Unknown"),
            customer_name=ocr_data.get("customer_name", "Unknown"),
            po_number=ocr_data.get("po_number"),
            invoice_date=datetime.datetime.fromisoformat(ocr_data.get("date", datetime.datetime.now().isoformat())),
            amount=ocr_data.get("amount", 0),
            tax=ocr_data.get("tax", 0),
            total_amount=ocr_data.get("total_amount", 0),
            status="pending",
            email_subject=email_subject,
            pdf_url=pdf_url or drive_link,
            drive_file_id=drive_file_id,
            ocr_data=ocr_data
        )
        
        db.add(invoice)
        db.flush()
        
        # Add line items
        for item in ocr_data.get("line_items", []):
            line_item = LineItem(
                invoice_id=invoice.id,
                description=item.get("description", ""),
                quantity=item.get("quantity", 0),
                unit_price=item.get("unit_price", 0),
                total_price=item.get("total_price", 0)
            )
            db.add(line_item)
        
        db.commit()
        return invoice.id
    except Exception as e:
        db.rollback()
        logger.error(f"Database error saving invoice: {str(e)}")
        return None
    finally:
        db.close()

def log_ingestion(
    email_subject: str,
    filename: str,
    email_from: str,
    email_date: datetime.datetime,
    status: str,
    drive_file_id: str = None,
    drive_link: str = None,
    error_message: str = None,
    invoice_id: int = None
):
    """Log email ingestion attempt"""
    db = SessionLocal()
    try:
        log = EmailIngestionLog(
            email_subject=email_subject,
            filename=filename,
            email_from=email_from,
            email_date=email_date,
            status=status,
            invoice_id=invoice_id,
            drive_file_id=drive_file_id,
            drive_link=drive_link,
            error_message=error_message
        )
        db.add(log)
        db.commit()
    except Exception as e:
        logger.error(f"Error logging ingestion: {str(e)}")
    finally:
        db.close()

# ================= HELPER FUNCTIONS =================

def decode_str(header_value: str) -> str:
    """Decode email header string"""
    if not header_value:
        return ""
    decoded_list = decode_header(header_value)
    text_parts = []
    for content, encoding in decoded_list:
        if isinstance(content, bytes):
            text_parts.append(content.decode(encoding or "utf-8", errors="ignore"))
        else:
            text_parts.append(str(content))
    return "".join(text_parts)

# ================= MAIN EMAIL PROCESSING =================

def connect_and_fetch():
    """Connect to Gmail, fetch emails, process invoices"""
    try:
        logger.info("🔗 Connecting to Gmail...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        
        # Create processed label if doesn't exist
        try:
            mail.create(PROCESSED_LABEL)
        except imaplib.IMAP4.error:
            pass
        
        mail.select("INBOX")
        status, messages = mail.search(None, "UNSEEN")
        
        if status != "OK" or not messages[0]:
            logger.info("✅ No unread emails found.")
            mail.logout()
            return {"message": "No emails to process", "count": 0}
        
        email_ids = messages[0].split()
        logger.info(f"📧 Found {len(email_ids)} unread emails")
        
        processed_count = 0
        
        for e_id in email_ids:
            try:
                # Decode email ID if it's bytes
                if isinstance(e_id, bytes):
                    e_id_str = e_id.decode()
                else:
                    e_id_str = str(e_id)
                
                _, msg_data = mail.fetch(e_id_str, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                
                subject = decode_str(msg.get("Subject", ""))
                email_from = decode_str(msg.get("From", ""))
                email_date = email.utils.parsedate_to_datetime(msg.get("Date", str(datetime.datetime.now())))
                subject_lower = subject.lower()
                
                logger.info(f"📧 Processing: '{subject}'")
                
                # Check keywords
                is_invoice_email = any(term in subject_lower for term in INVOICE_TERMS)
                if not is_invoice_email:
                    logger.info("   ❌ Skipped: No invoice keywords")
                    log_ingestion(subject, "N/A", email_from, email_date, "skipped", error_message="No invoice keywords")
                    continue
                
                # Check attachments
                valid_attachments = []
                for part in msg.walk():
                    content_disposition = str(part.get_content_disposition())
                    if "attachment" in content_disposition or "inline" in content_disposition:
                        fname = part.get_filename()
                        if fname and fname.lower().endswith(ALLOWED_EXTENSIONS):
                            valid_attachments.append((fname, part))
                
                if not valid_attachments:
                    logger.info("   ❌ Skipped: No valid attachments")
                    log_ingestion(subject, "N/A", email_from, email_date, "skipped", error_message="No valid attachments")
                    continue
                
                # Process attachments
                for filename, part in valid_attachments:
                    try:
                        email_bytes = part.get_payload(decode=True)
                        
                        # OCR Extract
                        ocr_data = ocr_and_extract_data(filename, email_bytes)
                        if not ocr_data:
                            raise Exception("OCR extraction failed")
                        
                        # Upload to Drive
                        clean_name = "".join(c for c in filename if c.isalnum() or c in "._- ")
                        new_name = f"{int(datetime.datetime.now().timestamp())}_{clean_name}"
                        drive_id, drive_link = upload_to_drive(email_bytes, new_name)
                        
                        # Save to DB
                        invoice_id = save_invoice_to_db(
                            ocr_data, drive_id, drive_link, subject, filename, pdf_url=drive_link
                        )
                        
                        # Log success
                        log_ingestion(
                            subject, filename, email_from, email_date,
                            "success", drive_id, drive_link, invoice_id=invoice_id
                        )
                        
                        logger.info(f"   ✅ Processed: {filename}")
                        processed_count += 1
                        
                    except Exception as e:
                        logger.error(f"   ❌ Error: {str(e)}")
                        log_ingestion(subject, filename, email_from, email_date, "failed", error_message=str(e))
                
                # Mark as read (DO NOT DELETE)
                mail.store(e_id_str, '+FLAGS', '\\Seen')
                # Optionally copy to processed label
                try:
                    mail.copy(e_id_str, PROCESSED_LABEL)
                except:
                    pass  # Label might not exist
                
            except Exception as e:
                logger.error(f"Email processing error: {str(e)}")
        
        # DO NOT expunge - keep all emails
        mail.logout()
        
        return {
            "message": f"Processing complete",
            "processed": processed_count,
            "total": len(email_ids)
        }
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        return {"error": str(e)}

# Async wrapper for API endpoint
async def process_emails_async():
    """Async wrapper for email processing"""
    return connect_and_fetch()
