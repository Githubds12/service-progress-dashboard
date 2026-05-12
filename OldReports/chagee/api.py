import requests
import json
import time

# Chagee API Configuration
BASE_URL = "https://api-sea.chagee.com"
SEND_OTP_ENDPOINT = f"{BASE_URL}/api/user-client/customer/sendVerifyCode"

def test_send_otp():
    # Placeholder for actual encrypted data and captcha parameters
    # In a real scenario, these would be generated dynamically
    payload = {
        "scene": "1",
        "sendObj": "J6rAjwj4jBfqCbPU3DmByw==", # Encrypted phone number example
        "sendType": "MOBILE",
        "captchaVerifyParam": json.dumps({
            "sceneId": "hoipvzll",
            "certifyId": "geUi7iAT8R",
            "deviceToken": "PLACEHOLDER_TOKEN"
        }),
        "data": "ENCRYPTED_DATA_BLOCK",
        "timestamp": int(time.time() * 1000),
        "smdid": "Bjs02TW8YmQRS1bkM3esAURhgrArRVvmM9W8vYzOskp4rPKqGAWrAkezFluicTJVp+CfrAmDJBYvJc8ek+dW8MA==",
        "sign": "TmQhkiyuBwWt23udcHJtbvQxm+Y="
    }

    headers = {
        "User-Agent": "Dart/3.10 (dart:io)",
        "Content-Type": "application/json",
        "apv": "3.33.0",
        "region": "MY",
        "channel": "APP",
        "os": "android"
    }

    print(f"[*] Sending test OTP request to {SEND_OTP_ENDPOINT}...")
    try:
        response = requests.post(SEND_OTP_ENDPOINT, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response Body:", response.text)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("errcode") == "0":
                print("[+] Successfully triggered OTP flow (or reached captcha gate).")
            else:
                print(f"[-] API Error: {data.get('errmsg')}")
        else:
            print(f"[-] Request Failed.")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    test_send_otp()
