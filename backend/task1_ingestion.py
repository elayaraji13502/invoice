import imaplib
import email
import datetime
from email.header import decode_header
import io
import os
import pickle

# Google API Imports
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ================= CONFIGURATION =================
# ⚠️ REPLACE WITH YOUR NEW APP PASSWORD
EMAIL_USER = "invoice.project01@gmail.com"
EMAIL_PASS = "pend sdym nkzx hrzg"
IMAP_SERVER = "imap.gmail.com"

# The Label (Folder) where processed emails will be moved
PROCESSED_LABEL = "Processed_Invoices"

GOOGLE_DRIVE_FOLDER_ID = "1LoRbKdiCsO4UpC2ahXcjdS4O5Nz3-ua_"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.pickle"

# Keywords to identify invoices
INVOICE_TERMS = [
    "invoice", "bill", "payment", "receipt",
    "total", "amount", "due", "credit note", "statement"
]

# Allowed file types (prevents uploading social media icons)
ALLOWED_EXTENSIONS = ('.pdf', '.docx', '.doc', '.xlsx', '.csv', '.jpg', '.png')

# Scope for Google Drive Access
SCOPES = ["https://www.googleapis.com/auth/drive"]
# =================================================


# ---------- GOOGLE DRIVE AUTHENTICATION (OAuth) ----------
def get_drive_service():
    """Authenticates the user and returns the Drive service."""
    creds = None
    token_path = TOKEN_FILE
    
    # Check if we have a saved token from a previous run
    if not os.path.exists(token_path):
        backend_token = os.path.join("backend", TOKEN_FILE)
        if os.path.exists(backend_token):
            token_path = backend_token

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = CREDENTIALS_FILE
            if not os.path.exists(credentials_path):
                backend_credentials = os.path.join("backend", CREDENTIALS_FILE)
                if os.path.exists(backend_credentials):
                    credentials_path = backend_credentials
                else:
                    raise FileNotFoundError(
                        f"❌ {CREDENTIALS_FILE} not found (checked root and backend/). Please provide OAuth client JSON."
                    )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

# Initialize Drive Service
drive_service = get_drive_service()


def upload_to_drive(file_bytes, filename):
    """Uploads a file to the specific Google Drive folder."""
    media = MediaIoBaseUpload(
        io.BytesIO(file_bytes),
        mimetype="application/octet-stream",
        resumable=True
    )

    metadata = {
        "name": filename,
        "parents": [GOOGLE_DRIVE_FOLDER_ID]
    }

    uploaded = drive_service.files().create(
        body=metadata,
        media_body=media,
        fields="id"
    ).execute()

    return uploaded["id"]


# ---------- HELPER FUNCTIONS ----------
def decode_str(header_value):
    """Decodes email headers (Subject, Filename) safely."""
    if not header_value: return ""
    decoded_list = decode_header(header_value)
    text_parts = []
    for content, encoding in decoded_list:
        if isinstance(content, bytes):
            text_parts.append(content.decode(encoding or "utf-8", errors="ignore"))
        else:
            text_parts.append(str(content))
    return "".join(text_parts)


# ---------- MAIN LOGIC ----------
def connect_and_fetch():
    print("ℹ️  Note: task1_ingestion uploads attachments to Drive and moves emails.")
    print("ℹ️  It does NOT create invoice rows in PostgreSQL used by the app UI.")
    print("ℹ️  For app invoice processing, use /ingestion/trigger via trigger_ingestion.py.")
    print("Connecting to Gmail...")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    
    # 1. Ensure the 'Processed' Label Exists
    try:
        mail.create(PROCESSED_LABEL)
    except imaplib.IMAP4.error:
        pass # Label likely already exists

    mail.select("INBOX")

    # 2. Search for Unread Emails
    status, messages = mail.search(None, "UNSEEN")
    
    if status != "OK" or not messages[0]:
        print("No unread emails found.")
        mail.logout()
        return

    email_ids = messages[0].split()
    print(f"Found {len(email_ids)} unread emails")

    for e_id in email_ids:
        try:
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])

            # --- Extract Subject ---
            subject = decode_str(msg.get("Subject", ""))
            subject_lower = subject.lower()

            # --- Extract Body (Text + HTML) ---
            body_content = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdisp = part.get_content_disposition()
                    if ctype in ["text/plain", "text/html"] and cdisp is None:
                        payload = part.get_payload(decode=True)
                        if payload: 
                            body_content += payload.decode(errors="ignore")
            else:
                payload = msg.get_payload(decode=True)
                if payload: 
                    body_content = payload.decode(errors="ignore")

            body_lower = body_content.lower()

            # --- Check Conditions ---
            found_terms = [t for t in INVOICE_TERMS if t in subject_lower or t in body_lower]
            
            # --- Extract Attachments ---
            valid_attachments = []
            for part in msg.walk():
                if part.get_content_disposition() == "attachment":
                    fname = decode_str(part.get_filename())
                    if fname and fname.lower().endswith(ALLOWED_EXTENSIONS):
                        valid_attachments.append((fname, part))

            is_invoice = bool(found_terms and valid_attachments)

            print(f"\n📧 Processing: {subject[:50]}...")
            
            if is_invoice:
                print("   ✅ Identified as Invoice.")
                for filename, part in valid_attachments:
                    # Clean filename
                    clean_name = "".join(c for c in filename if c.isalnum() or c in "._- ")
                    new_name = f"{int(datetime.datetime.now().timestamp())}_{clean_name}"
                    
                    # Upload
                    file_bytes = part.get_payload(decode=True)
                    drive_id = upload_to_drive(file_bytes, new_name)
                    print(f"      ☁ Uploaded: {new_name}")

                # --- MOVE TO PROCESSED LABEL ---
                result = mail.copy(e_id, PROCESSED_LABEL)
                if result[0] == 'OK':
                    mail.store(e_id, '+FLAGS', '\\Deleted') # Mark deleted in Inbox
                    print(f"      📥 Moved to '{PROCESSED_LABEL}'")
                else:
                    print(f"      ⚠️ Failed to move email.")
            
            else:
                print("   ⏭️  Skipping (Not an invoice). Left in Inbox.")
                # Optional: Mark as Read anyway? Uncomment below line if yes.
                # mail.store(e_id, "+FLAGS", "\\Seen") 

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # 3. Finalize: Remove emails marked as deleted
    mail.expunge()
    mail.logout()
    print("\nDone.")

if __name__ == "__main__":
    connect_and_fetch()