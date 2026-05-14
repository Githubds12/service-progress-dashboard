import requests
import json

url = "https://appapi.klook.com/v2/userapisrv/public/verification/code/send"

headers = {
    "x-signature": "ed8830c75044c975fc9acfcdbe89a8461c53483616986db6c17c1fd05989b4dc",
    "x-timestamp": "1777417495171",
    "x-klook-session-id": "MQ.3658eacbf74b44f2662b6c783605d443",
    "user-agent": "klook/7.43.0 (google-Pixel 7; android 35; Scale/6.00)",
    "content-type": "application/json"
}

def trigger_sms(phone, trace_id):
    payload = {
        "action": "login_register",
        "type": 1,
        "rcv": phone,
        "rcv_token": None,
        "is_resend": False,
        "payload": {
            "mobile": phone,
            "brand": "google",
            "carrier": "",
            "term_ids": [321]
        }
    }
    
    print(f"[*] Attempting to trigger SMS for {phone} (Trace ID: {trace_id})...")
    try:
        response = requests.post(url, headers=headers, json=payload, params={"trace_id": trace_id}, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        if response.status_code == 403:
            print("[!] Blocked by DataDome Captcha.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    trigger_sms("39-3517794696", "7c90450f-469d-4954-9e50-d7df43e6ca9b")
