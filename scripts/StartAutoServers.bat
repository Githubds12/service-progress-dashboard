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

echo [*] Starting DroidPilot Core Services...
pushd "c:\Users\Gorri\Documents\Reports\DroidPilot"
:: Start Web UI (FastAPI via uvicorn) and Mission Listener
set PYTHONPATH=src
start /min "DroidPilot Web" .venv\Scripts\python -m uvicorn droidpilot.ui.web.app:app --host 127.0.0.1 --port 7777
start /min "DroidPilot Listener" .venv\Scripts\python src/droidpilot/mission_listener.py
popd

echo [!] Auto Servers are now running in the background.
timeout /t 3 >nul
exit
