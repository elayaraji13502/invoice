@echo off
echo This script will reset your PostgreSQL password
echo.
echo Please run this command in Command Prompt as Administrator:
echo.
echo "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "ALTER USER postgres WITH PASSWORD 'postgres123';"
echo.
echo Or use pgAdmin to reset the password to: postgres123
pause
