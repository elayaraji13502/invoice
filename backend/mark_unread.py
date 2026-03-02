import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER", "invoice.project01@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = "imap.gmail.com"

# Connect to Gmail
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_USER, EMAIL_PASS)
mail.select("inbox")

# Search for all emails
_, message_numbers = mail.search(None, "ALL")
email_ids = message_numbers[0].split()

print(f"Total emails in inbox: {len(email_ids)}")

# Get last email and mark as unread
if email_ids:
    last_id = email_ids[-1]
    mail.store(last_id, '-FLAGS', '\\Seen')
    print(f"✅ Marked email {last_id.decode()} as unread")

mail.logout()
