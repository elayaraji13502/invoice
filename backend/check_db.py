from database import SessionLocal
from models import Invoice

db = SessionLocal()
invoices = db.query(Invoice).all()
print(f"Total invoices in database: {len(invoices)}")
for inv in invoices:
    print(f"  - Invoice #{inv.invoice_number}: {inv.vendor_name} - ${inv.total_amount}")
db.close()
