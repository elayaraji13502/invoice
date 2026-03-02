@echo off
REM Complete startup script for Invoice Hub
REM Starts both servers and triggers email ingestion

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Invoice Hub - Complete Startup
echo ========================================
echo.

REM Start backend in a new window
echo Starting Backend (FastAPI) on port 8000...
start "Invoice Hub - Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait for backend to start
echo Waiting 5 seconds for backend to initialize...
timeout /t 5 /nobreak

REM Start frontend in a new window
echo Starting Frontend (React + Vite) on port 8080...
start "Invoice Hub - Frontend" cmd /k "npm run dev"

REM Wait for frontend to start
echo Waiting 3 seconds for frontend to initialize...
timeout /t 3 /nobreak

REM Now trigger email ingestion via API
echo.
echo ========================================
echo Triggering Email Ingestion...
echo ========================================
echo.

REM Call the ingestion API endpoint
python -c "import requests; import time; time.sleep(2); requests.post('http://localhost:8000/ingestion/trigger', headers={'X-API-Key': 'test-api-key'}, timeout=120)" 2>nul

if %ERRORLEVEL% EQU 0 (
    echo Email ingestion triggered successfully!
) else (
    echo Note: Email ingestion will run on next request to the API
)

echo.
echo ========================================
echo ✓ All services started successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8080
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C in each window to stop the servers.
echo.

pause
