import asyncio
import os
import json
import httpx
import shutil
from datetime import datetime, timezone
from pathlib import Path

# Paths
BASE_DIR = Path(r"c:\Users\Gorri\Documents\Reports")
DATA_DIR = BASE_DIR / "data"
DASHBOARD_DIR = BASE_DIR / "dashboard"
LISTENER_STATUS = DATA_DIR / "listener_status.json"
HEALTH_OUTPUT = DATA_DIR / "system_health.json"

async def check_droidpilot():
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            resp = await client.get("http://localhost:7777/api/test/check")
            if resp.status_code == 200:
                return resp.json()
    except:
        pass
    return {"status": "offline"}

async def check_ollama():
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            resp = await client.get("http://localhost:11434/api/tags")
            if resp.status_code == 200:
                return {"status": "active", "url": "http://localhost:11434"}
    except:
        pass
    return {"status": "offline"}

async def check_adb():
    adb_path = shutil.which("adb")
    if not adb_path:
        return {"status": "error", "error": "ADB not in PATH"}
    try:
        proc = await asyncio.create_subprocess_exec(
            "adb", "devices",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        lines = stdout.decode().strip().split('\n')[1:]
        devices = [line.split('\t')[0] for line in lines if line.strip()]
        return {
            "status": "active" if devices else "no_devices",
            "device_count": len(devices),
            "devices": devices
        }
    except:
        return {"status": "error"}

def check_listener():
    if not LISTENER_STATUS.exists():
        return {"status": "inactive"}
    try:
        with open(LISTENER_STATUS, "r") as f:
            data = json.load(f)
            last_hb = datetime.fromisoformat(data["last_heartbeat"])
            diff = (datetime.now(timezone.utc) - last_hb).total_seconds()
            if diff < 120:
                return {"status": "active", "last_seen": data["last_heartbeat"]}
            else:
                return {"status": "stale", "last_seen": data["last_heartbeat"]}
    except:
        return {"status": "error"}

async def main():
    print("[*] Running System Diagnostics...")
    
    health = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "droidpilot": await check_droidpilot(),
        "ollama": await check_ollama(),
        "adb": await check_adb(),
        "listener": check_listener(),
        "dashboard_sync": {
            "last_sync": datetime.fromtimestamp(os.path.getmtime(DASHBOARD_DIR / "apkhunter_data.js")).isoformat() if (DASHBOARD_DIR / "apkhunter_data.js").exists() else None
        }
    }
    
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HEALTH_OUTPUT, "w") as f:
        json.dump(health, f, indent=4)
    
    print(f"[+] Health report saved to {HEALTH_OUTPUT}")

if __name__ == "__main__":
    asyncio.run(main())
