import imaplib
import email
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER", "invoice.project01@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

try:
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")

    # Get unread
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()

    if email_ids:
        e_id = email_ids[-1]
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        print(f"Subject: {msg.get('Subject', '')}")
        print("\nAttachments:")
        
        for part in msg.walk():
            disposition = str(part.get_content_disposition())
            print(f"  Disposition: {disposition}")
            fname = part.get_filename()
            if fname:
                print(f"  Filename: {fname}")
                print(f"  Content-Type: {part.get_content_type()}")

    mail.logout()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

input("Press enter to exit...")

