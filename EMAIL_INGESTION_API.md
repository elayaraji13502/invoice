# Email Ingestion API Documentation

## Overview

The Email Ingestion API automatically fetches invoices from Gmail, performs OCR extraction, uploads files to Google Drive, and stores invoice data in PostgreSQL.

## API Key Authentication

All email ingestion endpoints require API key authentication using the `X-API-Key` header.

### Getting Your API Key

Your API key is configured in the `.env` file:

```
API_KEY=invoice-hub-api-key-2024-secret-key
```

### Using the API Key

Include the key in the request header:

```bash
curl -X POST http://localhost:8000/ingestion/trigger \
  -H "X-API-Key: invoice-hub-api-key-2024-secret-key"
```

## Endpoints

### 1. Trigger Email Ingestion

**POST** `/ingestion/trigger`

Starts the email ingestion process. Processes unread Gmail emails with invoice keywords.

**Headers:**
```
X-API-Key: your-api-key
```

**Response:**
```json
{
  "success": true,
  "message": "Email ingestion completed",
  "result": {
    "message": "Processing complete",
    "processed": 5,
    "total": 8
  },
  "timestamp": "2026-02-27T10:30:45.123456"
}
```

**What it does:**
1. Connects to Gmail via IMAP
2. Fetches unread emails matching invoice keywords
3. Extracts PDF/Image attachments
4. Runs OCR using Mindee API
5. Uploads files to Google Drive
6. Saves invoice data to PostgreSQL
7. Moves processed emails to "Processed_Invoices" label

### 2. Get Ingestion Logs

**GET** `/ingestion-logs`

Retrieves the last 100 email ingestion attempts with their status.

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "emailSubject": "Invoice #INV-2024-001",
      "filename": "invoice.pdf",
      "emailFrom": "vendor@company.com",
      "status": "success",
      "driveLink": "https://drive.google.com/file/d/...",
      "errorMessage": null,
      "createdAt": "2026-02-27T10:30:45.123456"
    }
  ]
}
```

## Setup Requirements

### 1. Gmail Configuration

- Enable IMAP in Gmail settings
- Create an App Password (not your regular password)
- Set credentials in `.env`:
  ```
  EMAIL_USER=your-email@gmail.com
  EMAIL_PASS=your-app-password
  ```

### 2. Mindee OCR API

- Sign up at https://www.mindee.com
- Create a custom invoice model
- Add API key to `.env`:
  ```
  MINDEE_V2_API_KEY=your-mindee-api-key
  MINDEE_MODEL_ID=your-model-id
  ```

### 3. Google Drive Setup

- Create a Google Cloud project
- Enable Google Drive API
- Download OAuth credentials as `credentials.json`
- Place in backend folder
- Set folder ID in `.env`:
  ```
  GOOGLE_DRIVE_FOLDER_ID=your-folder-id
  ```

### 4. Database Setup

PostgreSQL tables are automatically created:
- `invoices` - Main invoice records
- `line_items` - Invoice line items
- `email_ingestion_logs` - Email processing history
- `invoice_audit_logs` - Invoice change tracking

## Frontend Integration

### Using the Ingestion Service

```typescript
import { triggerEmailIngestion, getIngestionLogs } from '@/services/ingestionService';

// Trigger ingestion
const result = await triggerEmailIngestion();
console.log(`Processed ${result.result.processed} emails`);

// Get ingestion history
const logs = await getIngestionLogs();
```

### Environment Variables

Add to `.env.local` or `.env`:
```
VITE_API_URL=http://localhost:8000
VITE_API_KEY=invoice-hub-api-key-2024-secret-key
```

## Invoice Keywords

The system recognizes emails containing:
- invoice, bill, payment, receipt, total, due
- order, statement, quote, estimate, contract
- subscription, purchase, transaction, amount, inv

## Supported File Types

- PDF (`.pdf`)
- Images (`.jpg`, `.jpeg`, `.png`)

## Database Schema

### Invoices Table
```sql
CREATE TABLE invoices (
  id SERIAL PRIMARY KEY,
  invoice_number VARCHAR UNIQUE,
  vendor_name VARCHAR,
  customer_name VARCHAR,
  invoice_date DATETIME,
  amount FLOAT,
  tax FLOAT,
  total_amount FLOAT,
  status VARCHAR (pending, accepted, rejected, in_review),
  drive_file_id VARCHAR,
  ocr_data JSON,
  created_at DATETIME DEFAULT NOW()
);
```

### Email Ingestion Logs Table
```sql
CREATE TABLE email_ingestion_logs (
  id SERIAL PRIMARY KEY,
  email_subject VARCHAR,
  filename VARCHAR,
  email_from VARCHAR,
  status VARCHAR (success, failed, skipped),
  drive_file_id VARCHAR,
  drive_link VARCHAR,
  error_message VARCHAR,
  created_at DATETIME DEFAULT NOW()
);
```

## Error Handling

If ingestion fails, check:
1. API key is correct
2. Gmail credentials are valid and IMAP is enabled
3. Google Drive folder ID is accessible
4. Mindee API key is valid
5. PostgreSQL connection is working

## Rate Limiting

- Gmail: Respects IMAP rate limits (~60 concurrent connections)
- Mindee: API limits apply based on your plan
- Google Drive: No strict rate limit for authenticated uploads

## Best Practices

1. **Security**: Keep API keys in environment variables, never commit to Git
2. **Monitoring**: Check ingestion logs regularly for failures
3. **Backup**: Google Drive provides automatic versioning
4. **Testing**: Start with test emails before processing production emails
5. **Scheduling**: Use a cron job or scheduler to run ingestion periodically

```bash
# Example: Run every hour using cron
0 * * * * curl -X POST http://localhost:8000/ingestion/trigger \
  -H "X-API-Key: your-key" >> /var/log/invoice-ingestion.log
```

## Troubleshooting

### No emails found
- Check that emails have invoice keywords
- Verify IMAP is enabled in Gmail
- Check that emails are actually unread

### OCR extraction fails
- Verify Mindee API key and model ID
- Check that files are valid PDFs/images
- Review Mindee model training

### Google Drive upload fails
- Verify folder permissions
- Check OAuth token hasn't expired
- Ensure folder ID is correct

### Database errors
- Run `python backend/create_tables.py` to recreate tables
- Check PostgreSQL connection
- Verify DB credentials in `.env`
