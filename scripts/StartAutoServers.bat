@echo off
echo ========================================
echo   STARTING DROIDPILOT AUTO SERVERS
echo ========================================
cd /d "c:\Users\Gorri\Documents\Reports"

set PYTHON_EXE="c:\Users\Gorri\Documents\Reports\.venv\Scripts\python.exe"

echo [*] Starting Secure Portal Backend (Port 10000)...
start /min "Portal Backend" %PYTHON_EXE% scripts\secure_agent_backend.py

echo [*] Running Initial Dashboard Update...
%PYTHON_EXE% scripts\update_dashboard.py

echo [*] Starting DroidPilot Core Services...
pushd "c:\Users\Gorri\Documents\Reports\DroidPilot"
set PYTHONPATH=src
start /min "DroidPilot Web" .venv\Scripts\python -m uvicorn droidpilot.ui.web.app:app --host 127.0.0.1 --port 7777
start /min "DroidPilot Listener" .venv\Scripts\python src/droidpilot/mission_listener.py
popd

echo [!] Auto Servers are now running in the background.
echo [!] Portal: http://localhost:10000
echo [!] DroidPilot: http://localhost:7777
timeout /t 5
exit


