@echo off
title DroidPilot Always-On Service
cd /d "c:\Users\Gorri\Documents\Reports\DroidPilot"

echo [*] Starting DroidPilot Web UI...
start /min cmd /c "python -m droidpilot.main"

echo [*] Starting Mission Listener...
start /min cmd /c "python src/droidpilot/mission_listener.py"

echo [!] DroidPilot Services Active.
pause
