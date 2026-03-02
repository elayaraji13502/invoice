"""
Create sample invoices for testing
"""
from database import SessionLocal
from models import Invoice, LineItem
from datetime import datetime

db = SessionLocal()

# Sample invoices
invoices_data = [
    {
        "invoice_number": "INV-2024-001",
        "vendor_name": "ABC Supplies Inc.",
        "vendor_email": "vendor@abcsupplies.com",
        "customer_name": "John Manufacturing",
        "po_number": "PO-123456",
        "invoice_date": datetime(2024, 2, 1),
        "amount": 5000.00,
        "tax": 500.00,
        "total_amount": 5500.00,
        "status": "pending",
        "email_subject": "Invoice for February 2024",
        "line_items": [
            {"description": "Widget A", "quantity": 100, "unit_price": 25.00, "total_price": 2500.00},
            {"description": "Widget B", "quantity": 100, "unit_price": 25.00, "total_price": 2500.00},
        ]
    },
    {
        "invoice_number": "INV-2024-002",
        "vendor_name": "XYZ Distributors",
        "vendor_email": "sales@xyzdist.com",
        "customer_name": "Jane Trading",
        "po_number": "PO-789012",
        "invoice_date": datetime(2024, 2, 5),
        "amount": 3200.00,
        "tax": 320.00,
        "total_amount": 3520.00,
        "status": "pending",
        "email_subject": "Invoice #INV-2024-002",
        "line_items": [
            {"description": "Component X", "quantity": 50, "unit_price": 32.00, "total_price": 1600.00},
            {"description": "Component Y", "quantity": 50, "unit_price": 32.00, "total_price": 1600.00},
        ]
    },
    {
        "invoice_number": "INV-2024-003",
        "vendor_name": "Tech Solutions Ltd.",
        "vendor_email": "billing@techsol.com",
        "customer_name": "Global Corp",
        "po_number": "PO-456789",
        "invoice_date": datetime(2024, 2, 10),
        "amount": 8750.00,
        "tax": 875.00,
        "total_amount": 9625.00,
        "status": "in_review",
        "email_subject": "Payment Request - Invoice INV-2024-003",
        "line_items": [
            {"description": "Software License (Annual)", "quantity": 1, "unit_price": 8750.00, "total_price": 8750.00},
        ]
    },
]

try:
    for inv_data in invoices_data:
        line_items = inv_data.pop("line_items")
        
        invoice = Invoice(**inv_data)
        db.add(invoice)
        db.flush()  # Get the invoice ID
        
        # Add line items
        for item in line_items:
            line_item = LineItem(invoice_id=invoice.id, **item)
            db.add(line_item)
    
    db.commit()
    print("✓ Sample invoices created successfully!")
    
except Exception as e:
    db.rollback()
    print(f"✗ Error: {e}")
finally:
    db.close()
