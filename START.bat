@echo off
REM ============================================
REM Invoice Hub - Complete Automated Startup
REM ============================================
REM This script:
REM 1. Starts backend on port 8000
REM 2. Starts frontend on port 8080
REM 3. Waits for both to be ready
REM 4. Automatically triggers email ingestion
REM 5. Opens browser to the app
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ============================================
echo   Invoice Hub - COMPLETE STARTUP
echo ============================================
echo.
echo This will:
echo   - Start Backend (FastAPI) on port 8000
echo   - Start Frontend (React) on port 8080
echo   - Trigger email ingestion
echo   - Open browser to http://localhost:8080
echo.
echo ============================================
echo.

REM Start backend in a new window
echo [1/4] Starting Backend Server...
start "Invoice Hub Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait 5 seconds for backend to initialize
timeout /t 5 /nobreak

REM Start frontend in a new window
echo [2/4] Starting Frontend Server...
start "Invoice Hub Frontend" cmd /k "npm run dev"

REM Wait 3 seconds for frontend to initialize
timeout /t 3 /nobreak

echo [3/4] Triggering Email Ingestion...
REM Call the ingestion script with Python
python trigger_ingestion.py
if %ERRORLEVEL% NEQ 0 (
	echo [WARN] Email ingestion did not complete successfully. Check backend window logs.
) else (
	echo [OK] Email ingestion completed successfully.
)

echo [4/4] Opening browser...
REM Open browser (this will work on most Windows systems)
timeout /t 2 /nobreak
start "" "http://localhost:8080"

echo.
echo ============================================
echo   ✓ Startup Complete!
echo ============================================
echo.
echo Services Running:
echo   - Backend:  http://localhost:8000
echo   - Frontend: http://localhost:8080
echo   - API Docs: http://localhost:8000/docs
echo.
echo Browser should open automatically at:
echo   http://localhost:8080
echo.
echo Email ingestion can be run anytime with: python trigger_ingestion.py
echo.
echo To stop all servers: Close each command window
echo To run ingestion again: python trigger_ingestion.py
echo.
echo ============================================
echo.

pause
