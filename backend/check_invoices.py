from database import SessionLocal
from models import Invoice, EmailIngestionLog

db = SessionLocal()

print(f"Total invoices: {db.query(Invoice).count()}")

latest_invoices = db.query(Invoice).order_by(Invoice.id.desc()).limit(3).all()
print("\nLatest invoices:")
for inv in latest_invoices:
    print(f"  ID: {inv.id}, Number: {inv.invoice_number}, Vendor: {inv.vendor_name}, Created: {inv.created_at}")

latest_logs = db.query(EmailIngestionLog).order_by(EmailIngestionLog.created_at.desc()).limit(5).all()
print("\nLatest ingestion logs:")
for log in latest_logs:
    print(f"  {log.created_at} - {log.status} - {log.filename} - InvoiceID: {log.invoice_id} - Error: {log.error_message}")

db.close()
