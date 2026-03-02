"""
Mark processed emails as unread so they can be reprocessed
"""
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER", "invoice.project01@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "pend sdym nkzx hrzg")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")

def mark_recent_as_unread(count=5):
    """Mark the most recent N emails in Processed_Invoices as unread"""
    try:
        print(f"🔗 Connecting to Gmail...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        
        # Check Processed_Invoices label
        mail.select("Processed_Invoices")
        status, messages = mail.search(None, "ALL")
        
        if status != "OK" or not messages[0]:
            print("❌ No emails found in Processed_Invoices")
            mail.logout()
            return
        
        email_ids = messages[0].split()
        recent_ids = email_ids[-count:] if len(email_ids) >= count else email_ids
        
        print(f"📧 Found {len(email_ids)} emails in Processed_Invoices")
        print(f"🔄 Marking {len(recent_ids)} most recent emails as UNREAD...")
        
        for e_id in recent_ids:
            if isinstance(e_id, bytes):
                e_id_str = e_id.decode()
            else:
                e_id_str = str(e_id)
            
            # Remove SEEN flag to mark as unread
            mail.store(e_id_str, '-FLAGS', '\\Seen')
            print(f"   ✅ Marked email {e_id_str} as unread")
        
        # Also move them back to INBOX
        print(f"\n📬 Moving emails back to INBOX...")
        for e_id in recent_ids:
            if isinstance(e_id, bytes):
                e_id_str = e_id.decode()
            else:
                e_id_str = str(e_id)
            
            mail.copy(e_id_str, 'INBOX')
            print(f"   ✅ Copied email {e_id_str} to INBOX")
        
        mail.logout()
        print("\n✅ Done! Emails are now unread and in INBOX.")
        print("   Run the ingestion again to reprocess them.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    mark_recent_as_unread(count)
