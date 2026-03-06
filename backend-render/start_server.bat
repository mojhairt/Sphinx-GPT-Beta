@echo off
echo ==========================================
echo  Sphinx-SCA Backend Server - Starting...
echo ==========================================
echo.

cd /d "%~dp0"

echo Stopping any existing server on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING 2^>nul') do taskkill /F /PID %%a 2>nul

echo.
echo Starting backend on http://127.0.0.1:8000
echo.
"C:\Users\Administrator\AppData\Local\Programs\Python\Python313\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
pause
