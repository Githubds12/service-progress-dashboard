import os
import json
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_BASE = "http://51.195.24.179:8092/api"
EMAIL = os.getenv("PULSE_EMAIL", "deepanshu@test.com")
PASS = os.getenv("PULSE_PASS", "deep@nshu")
JS_FILE_PATH = "dashboard/apkhunter_data.js"

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
    '069a1a08-cd0d-4c06-af9f-7ed514994d04': 'shellotp',
    'fe525436-57c7-4daf-9d6a-d2f023e1b717': 'cloudotp',
    '587f6988-cc68-491d-8904-770e9ffa4c24': 'appie',
    '7c6446d4-bdab-4615-8242-b3cd64637b2b': 'tamsg',
    'f5037e17-906f-4656-ac11-6d2c28f5f2b2': 'blnance',
    '0d314601-f322-4a23-84b5-f7f49dc8a690': 'infsoms',
    '43945afe-0cc1-4d4b-a9d6-50e43a818209': 'hacher',
    '9962429d-1dd1-4a5f-aef3-86089b3959f0': 'whitelist',
    'b7ab99b2-14ee-4f85-80e4-b2a13be3a58c': 'carry1st',
    'c61cc81d-a387-4c71-8612-dcd0260c201c': 'gm-sms',
    'd3c848d1-8769-4896-9c67-8886a0d204b6': 'qpsms'
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

def main():
    print("[*] Cloud Rotatory Sync Started")
    
    # 1. Read existing JS file
    if not os.path.exists(JS_FILE_PATH):
        print(f"[!] File not found: {JS_FILE_PATH}")
        return
        
    with open(JS_FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    json_str = content.replace("window.apkhunterData = ", "").strip()
    if json_str.endswith(";"):
        json_str = json_str[:-1]
        
    try:
        data = json.loads(json_str)
    except Exception as e:
        print(f"[!] Error parsing JSON from {JS_FILE_PATH}: {e}")
        return

    # Map array to dict for quick lookups
    target_dict = {item['id']: item for item in data if 'id' in item}
    
    token = get_token()
    if not token:
        print("[!] Could not get API token.")
        return
        
    updated = False
    
    # 2. Fetch new messages and inject
    for sid, name in ROTATORY_SERVICES.items():
        if sid not in target_dict:
            continue
            
        target = target_dict[sid]
        msg = fetch_message(token, sid)
        
        if not msg:
            continue
            
        history = target.get('history', [])
        last_msg = history[-1]['message'] if history else None
        
        # Current message in UI is technically `target['sms']`, but our unified log logic 
        # puts target['sms'] at the top of the history list UI as LATEST.
        # So if msg != target['sms'], we have a new message.
        if msg != target.get('sms'):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            safe_msg = msg
            print(f"[+] NEW MESSAGE for {name} ({sid}): {safe_msg[:50]}...")
            
            # The *old* sms becomes history
            old_sms = target.get('sms')
            if old_sms:
                # If the old sms isn't already the last item in history, append it
                if not history or history[-1]['message'] != old_sms:
                    history.append({
                        "timestamp": target.get('last_updated', timestamp),
                        "message": old_sms
                    })
                    
            # Update target
            target['sms'] = msg
            target['last_updated'] = timestamp
            
            # Keep only last 20 messages to prevent bloat
            if len(history) > 20:
                history = history[-20:]
                
            target['history'] = history
            updated = True
            
    # 3. Always update last_sync.json for the dashboard
    status_file = "dashboard/last_sync.json"
    status_data = {
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "SUCCESS",
        "message": "Cloud sync complete." if updated else "No new messages."
    }
    with open(status_file, "w") as f:
        json.dump(status_data, f, indent=4)

    # 4. Write back if updated
    if updated:
        with open(JS_FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(f"window.apkhunterData = {json.dumps(data, indent=4, ensure_ascii=False)};\n")
        print("[*] Successfully updated apkhunter_data.js")
    else:
        print("[-] No new messages found.")

if __name__ == "__main__":
    main()
