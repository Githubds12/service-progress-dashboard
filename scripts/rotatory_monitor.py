import requests
import json
import time
import os
import sys
from datetime import datetime

# Force UTF-8 encoding for stdout
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---
API_BASE = "http://51.195.24.179:8092/api"
EMAIL = "deepanshu@test.com"
PASS = "deep@nshu"
HISTORY_PATH = r"C:\HTB-Notes-Portal\sms_history.json"
INTERVAL = 600  # 10 minutes

# Targets provided by user
ROTATORY_SERVICES = {
    '49fbcfe1-b82d-41ad-a214-46a5e4b06310': 'tokens',
    '0aabd800-8891-40f3-b5af-2eac9085574f': 'iatsms',
    '42fd3ec7-08a1-4cad-81cf-b2f669880c4f': 'Byteplus',
    'd07ee58f-63b4-41ad-9d91-764988964ebd': 'qsms',
    '8d0926e7-5324-4d63-b049-3a3f5ab42e8c': 'nxcomm',
    'd94e9010-0171-4305-8f47-c5e28cf8ec06': 'infosms',
    'dea9e292-dde0-4c86-9d36-1c54a9cbd2db': 'nxcsms',
    '89a73875-0246-4caf-b4b2-a14a9d506b5d': 'hcloud',
    '2b2791af-2bd5-4627-9f24-cb7aa7b62e76': 'msverify',
    '34c46101-4370-4abc-be0f-33d5f276db6e': 'SMS',
    '678b53a7-f77f-428f-ad0f-fe826acd926f': 'smsverify',
    '41201c51-5d64-448a-b7ab-f61c26677e72': 'twverify',
    'fbbaa989-6a1b-4037-baad-5f1288b132f9': 'tbc sms',
    '7f8ecc98-8c55-4fcd-8b56-a4ee04344ae0': 'smsto',
    'ef4f0634-5039-468c-b266-ee5b327771c4': 'wave',
    '71a9373e-45ae-4113-af09-3e56d06a1e19': 'alisms',
    'e05e03a5-8e71-4028-88a4-3922863838f3': 'authmsg',
    '430dde58-e96f-405f-89d1-91277ad095fd': 'authsms',
    'ed65e20e-4d64-4684-b9bd-ede11a19140c': 'grab',
    'dcf6658c-2536-4ab4-be0d-6da9d15bdd79': 'garena',
    'f6fb02b3-7ef3-439d-b977-41e2a1fa0b57': 'notice',
    'f5e5c9ad-b0b1-4b44-a80f-934946f9a097': 'mtsms',
    'f21f0bd8-65c7-4f72-9326-60f64e71af32': 'unsms',
    'f676831f-36d6-450c-9d9c-eed903ee3a43': 'ssosms',
    '069a1a08-cd0d-4c06-af9f-7ed514994d04': 'shellotp'
}

def get_token():
    try:
        res = requests.post(f"{API_BASE}/auth/login", json={"email": EMAIL, "password": PASS}, timeout=15)
        return res.json().get("access_token")
    except Exception as e:
        print(f"[{datetime.now()}] Login Error: {e}")
        return None

def fetch_message(token, service_id):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{API_BASE}/services/{service_id}"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            return res.json().get("sample_message")
    except Exception as e:
        print(f"[{datetime.now()}] Fetch Error ({service_id}): {e}")
    return None

def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_history(history):
    with open(HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)

def monitor():
    print(f"[*] Rotatory SMS Monitor Started. Interval: {INTERVAL}s")
    print(f"[*] Monitoring {len(ROTATORY_SERVICES)} services.")
    
    while True:
        token = get_token()
        if not token:
            print("[!] Could not get token. Retrying in 60s...")
            time.sleep(60)
            continue
            
        history = load_history()
        updated = False
        
        for sid, name in ROTATORY_SERVICES.items():
            msg = fetch_message(token, sid)
            if not msg:
                continue
                
            # Get current history for this service
            s_history = history.get(sid, [])
            
            # Check if this message is already the latest one
            last_msg = s_history[-1]['message'] if s_history else None
            
            if msg != last_msg:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Handle potential encoding issues in console output
                safe_msg = msg.encode('ascii', 'ignore').decode('ascii')
                print(f"[+] NEW MESSAGE for {name} ({sid}): {safe_msg[:50]}...")
                s_history.append({
                    "timestamp": timestamp,
                    "message": msg
                })
                # Keep only last 50 messages to prevent bloat
                if len(s_history) > 50:
                    s_history = s_history[-50:]
                    
                history[sid] = s_history
                updated = True
            else:
                # print(f"[-] No change for {name}.")
                pass
        
        if updated:
            save_history(history)
            print(f"[*] History updated at {datetime.now()}.")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    monitor()
