import requests
import json
import uuid

url = "https://httpproxy102.buz-app.com/com.buz.idl.login.service.BuzNetLoginService/sendSmsCode"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Buz/1.98.0 (Android; 15; Google Pixel 7)"
}

def trigger_sms(phone_full):
    # phone_full example: "39-3513534110"
    trace_id = uuid.uuid4().hex
    payload = {
        "request": {
            "installedApp": [1],
            "phone": phone_full,
            "phoneInputType": 5,
            "resend": False,
            "riskParams": {
                "mediaChannel": "Organic",
                "storeChannel": "google"
            },
            "traceId": trace_id,
            "type": 3
        }
    }
    
    print(f"[*] Triggering SMS for {phone_full}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    trigger_sms("39-3513534110")
