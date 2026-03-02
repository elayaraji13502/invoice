@echo off
REM Start both Backend and Frontend servers
REM This batch file runs both servers in separate windows

echo.
echo ========================================
echo Invoice Hub - Backend & Frontend
echo ========================================
echo.
echo Starting services on:
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:8080
echo.

REM Start backend in a new window
echo Starting Backend (FastAPI)...
start "Invoice Hub - Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak

REM Start frontend in a new window
echo Starting Frontend (Vite + React)...
start "Invoice Hub - Frontend" cmd /k "npm run dev"

echo.
echo Both servers are starting...
echo Press Ctrl+C in each window to stop the servers.
echo.
