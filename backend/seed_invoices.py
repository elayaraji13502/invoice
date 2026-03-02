from database import SessionLocal
from models import Invoice, LineItem
from datetime import datetime, timedelta

db = SessionLocal()

# Clear existing data
db.query(LineItem).delete()
db.query(Invoice).delete()
db.commit()

# Create sample invoices
sample_invoices = [
    {
        "invoice_number": "INV-2024-001",
        "vendor_name": "Acme Corporation",
        "vendor_email": "billing@acme.com",
        "customer_name": "ABC Company",
        "po_number": "PO-2024-001",
        "invoice_date": datetime.now() - timedelta(days=5),
        "amount": 5000.00,
        "tax": 500.00,
        "total_amount": 5500.00,
        "status": "pending",
        "email_subject": "Invoice for Services - January 2024",
        "line_items": [
            {"description": "Consulting Services", "quantity": 40, "unit_price": 100, "total_price": 4000},
            {"description": "Software License", "quantity": 1, "unit_price": 1000, "total_price": 1000},
        ]
    },
    {
        "invoice_number": "INV-2024-002",
        "vendor_name": "Tech Solutions Ltd",
        "vendor_email": "invoices@techsol.com",
        "customer_name": "XYZ Industries",
        "po_number": "PO-2024-002",
        "invoice_date": datetime.now() - timedelta(days=3),
        "amount": 3500.00,
        "tax": 350.00,
        "total_amount": 3850.00,
        "status": "in_review",
        "email_subject": "Monthly Invoice - February 2024",
        "line_items": [
            {"description": "Cloud Hosting", "quantity": 1, "unit_price": 2000, "total_price": 2000},
            {"description": "Support Services", "quantity": 5, "unit_price": 300, "total_price": 1500},
        ]
    },
    {
        "invoice_number": "INV-2024-003",
        "vendor_name": "Office Supplies Plus",
        "vendor_email": "sales@officesupplies.com",
        "customer_name": "Main Office",
        "po_number": "PO-2024-003",
        "invoice_date": datetime.now() - timedelta(days=2),
        "amount": 1200.00,
        "tax": 120.00,
        "total_amount": 1320.00,
        "status": "pending",
        "email_subject": "Office Equipment Order #12345",
        "line_items": [
            {"description": "Desk Chairs (4x)", "quantity": 4, "unit_price": 250, "total_price": 1000},
            {"description": "Shipping", "quantity": 1, "unit_price": 200, "total_price": 200},
        ]
    },
    {
        "invoice_number": "INV-2024-004",
        "vendor_name": "Marketing Agency Pro",
        "vendor_email": "billing@marketingpro.com",
        "customer_name": "Brand Department",
        "po_number": "PO-2024-004",
        "invoice_date": datetime.now() - timedelta(days=10),
        "amount": 7500.00,
        "tax": 750.00,
        "total_amount": 8250.00,
        "status": "accepted",
        "email_subject": "Q1 Marketing Campaign Invoice",
        "line_items": [
            {"description": "Social Media Management", "quantity": 3, "unit_price": 2000, "total_price": 6000},
            {"description": "Graphics Design", "quantity": 2, "unit_price": 750, "total_price": 1500},
        ]
    },
    {
        "invoice_number": "INV-2024-005",
        "vendor_name": "Logistics & Shipping Co",
        "vendor_email": "invoices@logisticco.com",
        "customer_name": "Warehouse",
        "po_number": "PO-2024-005",
        "invoice_date": datetime.now() - timedelta(days=1),
        "amount": 2800.00,
        "tax": 280.00,
        "total_amount": 3080.00,
        "status": "rejected",
        "email_subject": "Shipping Services - February Deliveries",
        "line_items": [
            {"description": "Domestic Shipping", "quantity": 25, "unit_price": 100, "total_price": 2500},
            {"description": "Tracking Service", "quantity": 1, "unit_price": 300, "total_price": 300},
        ]
    },
]

# Insert invoices
for inv_data in sample_invoices:
    line_items_data = inv_data.pop("line_items")
    
    invoice = Invoice(**inv_data)
    db.add(invoice)
    db.flush()  # Get the invoice ID
    
    # Add line items
    for item_data in line_items_data:
        item = LineItem(invoice_id=invoice.id, **item_data)
        db.add(item)

db.commit()
db.close()

print("✅ Sample invoices created successfully!")
print(f"Created {len(sample_invoices)} invoices with line items")
