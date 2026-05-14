import requests
import json

url = "https://appapi.abcdstable.com/v1/msg/verifyCode/send"

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) ...",
    "Content-Type": "application/json; charset=utf-8",
    "x-sign": "EDGE-V1-1-6yuwcdZQzTXwhzLWIItQKnxuIIkJ9R0UhmiEeX3QjW0=",
    "deviceId": "a177741635452379781998816"
}

def trigger_sms(phone, verify_key):
    payload = {
        "areaCode": "39",
        "bizType": "REGISTER_MOBILE",
        "address": phone,
        "sendType": "SMS",
        "verifyKey": verify_key,
        "retry": 1
    }
    
    print(f"[*] Attempting to trigger SMS for {phone}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print("Status Code:", response.status_code)
        print("Response:", response.text)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    # verify_key is obtained after solving the captcha via check-login-name
    trigger_sms("3522956432", "hmac_CwgCEiA2REY2QkJFOTM3QUM2N0UyMTJEREJCQjEzQkNFNTgyNxoSc2VydmljZS1ncm91cC1kYXRhDBJb...")
