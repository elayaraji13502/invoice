# 🚀 Invoice Hub - Complete Startup Solutions

## The Problem You Had
You wanted to run both backend AND frontend together without starting them separately, and also have the email ingestion run automatically.

## ✅ Solutions Available

### **EASIEST WAY - Just Click! 🖱️**
**File:** `START.bat`
- Double-click this file in your project root
- It will:
  1. Start backend (port 8000)
  2. Start frontend (port 8080)
  3. Automatically trigger email ingestion
  4. Open browser to the app
- Everything happens automatically!

---

### **ALTERNATIVE - Using npm command**
```bash
npm run start:all
```
- Starts both backend and frontend in ONE terminal
- Shows logs from both servers
- Then manually run: `python trigger_ingestion.py` in another terminal
- Or trigger via: http://localhost:8000/docs (use the POST /ingestion/trigger endpoint)

---

### **ALTERNATIVE - For developers**
```bash
# Terminal 1: Start both servers
npm run start:all

# Terminal 2: Trigger ingestion
python trigger_ingestion.py
```

---

## 📋 What Each New File Does

| File | Purpose |
|------|---------|
| `START.bat` | 🌟 **Main startup** - Does everything automatically |
| `start-all.bat` | Starts both servers in separate windows |
| `start-servers.bat` | Alternative starter script |
| `trigger_ingestion.py` | Manually trigger email ingestion |
| `QUICKSTART.md` | Complete documentation |
| `package.json` | Updated with `start:all` command |

---

## 🎯 Recommended Workflow

1. **First time**: 
   ```bash
   npm install
   npm install --save-dev concurrently
   ```

2. **Every time you want to run**: 
   - **Double-click:** `START.bat` (Windows)
   - **Or run:** `npm run start:all` + `python trigger_ingestion.py`

3. **What happens**:
   - ✅ Backend starts on http://localhost:8000
   - ✅ Frontend starts on http://localhost:8080
   - ✅ Email ingestion runs automatically
   - ✅ Browser opens to the app
   - ✅ You can start reviewing invoices

---

## 🔄 Email Ingestion Workflow

The `trigger_ingestion.py` script:
1. Waits for backend to be ready
2. Calls `/ingestion/trigger` API endpoint
3. Backend connects to Gmail
4. Fetches unread invoice emails
5. Extracts data with Mindee OCR
6. Uploads files to Google Drive
7. Saves to PostgreSQL database
8. Invoices appear in Review Queue

---

## 📊 Current Status

**What's implemented:**
- ✅ Backend API (FastAPI)
- ✅ Frontend UI (React + Vite)
- ✅ Email ingestion system
- ✅ OCR with Mindee
- ✅ Google Drive integration
- ✅ PostgreSQL database
- ✅ Invoice review workflow
- ✅ Decision history tracking
- ✅ User authentication
- ✅ **Complete startup automation** (NEW!)
- ✅ **Email ingestion auto-trigger** (NEW!)

---

## 🎓 Examples

### Example 1: Simple startup
```bash
START.bat
```
That's it! Everything else is automatic.

### Example 2: If START.bat doesn't work
```bash
npm run start:all
# Wait for both servers to start
# Then in a new terminal:
python trigger_ingestion.py
```

### Example 3: Manual API call
```bash
curl -X POST http://localhost:8000/ingestion/trigger \
  -H "X-API-Key: test-api-key"
```

---

## ⚠️ Important Notes

1. **First time setup**: Make sure you've installed dependencies:
   ```bash
   npm install
   npm install --save-dev concurrently
   ```

2. **Environment variables**: Check `.env` file has:
   - Gmail credentials
   - Database connection details
   - Mindee API key
   - Google Drive folder ID

3. **Ports**: Make sure 8000 and 8080 are available

4. **Database**: PostgreSQL must be running

---

## 🆘 Troubleshooting

**START.bat doesn't work?**
- Right-click → Run as Administrator
- Or use: `npm run start:all` instead

**Email ingestion doesn't run?**
- Check `.env` file for valid Gmail app password
- Run manually: `python trigger_ingestion.py`
- Check logs in browser at http://localhost:8000/docs

**Port already in use?**
- Change in package.json and batch files
- Or: `netstat -ano | findstr :8000` to find what's using it

---

## 📚 Next Steps

1. **Double-click START.bat** to start everything
2. **Login** with reviewer / test123
3. **Check Review Queue** for new invoices
4. **Click Review** to see invoice details
5. **Accept/Reject** invoices
6. **Check Decision History** to see your reviews

Done! 🎉
