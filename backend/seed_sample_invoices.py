"""
Create sample invoices directly in database for testing
"""
from database import SessionLocal
from models import Invoice, LineItem
from datetime import datetime, timedelta

db = SessionLocal()

try:
    # Clear existing
    db.query(LineItem).delete()
    db.query(Invoice).delete()
    db.commit()
    
    invoices_data = [
        {
            "invoice_number": "INV-2025-001",
            "vendor_name": "Tech Solutions Inc.",
            "vendor_email": "billing@techsolutions.com",
            "customer_name": "Your Company",
            "invoice_date": datetime.now(),
            "amount": 4500.00,
            "tax": 1000.00,
            "total_amount": 5500.00,
            "status": "pending",
            "drive_file_id": "drive_001",
            "line_items": [
                {"description": "Software Development Services", "quantity": 40, "unit_price": 100.00, "total_price": 4000.00},
                {"description": "Technical Support", "quantity": 10, "unit_price": 50.00, "total_price": 500.00},
            ]
        },
        {
            "invoice_number": "INV-2025-002",
            "vendor_name": "Office Supplies Co.",
            "vendor_email": "invoices@officesupplies.com",
            "customer_name": "Your Company",
            "invoice_date": datetime.now(),
            "amount": 2000.00,
            "tax": 150.50,
            "total_amount": 2150.50,
            "status": "pending",
            "drive_file_id": "drive_002",
            "line_items": [
                {"description": "Office Chairs (5x)", "quantity": 5, "unit_price": 250.00, "total_price": 1250.00},
                {"description": "Desk Lamps", "quantity": 10, "unit_price": 45.00, "total_price": 450.00},
                {"description": "Stationery Pack", "quantity": 20, "unit_price": 25.00, "total_price": 500.00},
            ]
        },
        {
            "invoice_number": "INV-2025-003",
            "vendor_name": "Cloud Services Ltd",
            "vendor_email": "billing@cloudservices.com",
            "customer_name": "Your Company",
            "invoice_date": datetime.now(),
            "amount": 8500.00,
            "tax": 499.99,
            "total_amount": 8999.99,
            "status": "approved",
            "drive_file_id": "drive_003",
            "line_items": [
                {"description": "Monthly Cloud Hosting (3 servers)", "quantity": 3, "unit_price": 500.00, "total_price": 1500.00},
                {"description": "CDN & Bandwidth", "quantity": 1, "unit_price": 2000.00, "total_price": 2000.00},
                {"description": "Database Services", "quantity": 1, "unit_price": 3000.00, "total_price": 3000.00},
                {"description": "24/7 Support Plan", "quantity": 1, "unit_price": 1500.00, "total_price": 1500.00},
            ]
        },
    ]
    
    for inv_data in invoices_data:
        line_items = inv_data.pop("line_items")
        invoice = Invoice(**inv_data)
        db.add(invoice)
        db.flush()  # Get the ID
        
        for item_data in line_items:
            line_item = LineItem(invoice_id=invoice.id, **item_data)
            db.add(line_item)
    
    db.commit()
    print(f"✅ Created {len(invoices_data)} sample invoices")
    
    # Verify
    count = db.query(Invoice).count()
    print(f"Total invoices in database: {count}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
