@echo off
echo ========================================
echo   STARTING DROIDPILOT AUTO SERVERS
echo ========================================
cd /d "c:\Users\Gorri\Documents\Reports"

echo [*] Starting Dashboard Server on Port 8000...
start /b python dump\serve_dashboard.py

echo [*] Running Initial Dashboard Update...
python scripts\update_dashboard.py

echo [*] Starting API Portal (Monitor Mode)...
:: start /b python scripts\api_portal.py --monitor (if such mode exists)

echo [!] Auto Servers are now running in the background.
exit
