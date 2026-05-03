@echo off
echo ========================================
echo   STARTING DROIDPILOT AUTO SERVERS
echo ========================================
cd /d "c:\Users\Gorri\Documents\Reports"

set PYTHON_EXE="c:\Users\Gorri\Documents\Reports\.venv\Scripts\python.exe"

echo [*] Starting Dashboard Server on Port 8000...
:: Use start without /b to ensure it lives in its own process, minimized
start /min "" %PYTHON_EXE% dump\serve_dashboard.py

echo [*] Running Initial Dashboard Update...
%PYTHON_EXE% scripts\update_dashboard.py

echo [*] Starting API Portal (Monitor Mode)...
:: %PYTHON_EXE% scripts\api_portal.py --monitor

echo [!] Auto Servers are now running in the background.
timeout /t 3 >nul
exit
