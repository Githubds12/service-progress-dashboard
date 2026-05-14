import requests
import json

# Aegean Airlines API Automation
# Endpoint: https://mobapi.aegeanair.com/connect/send-otp

BASE_URL = "https://mobapi.aegeanair.com"
HEADERS = {
    "x-mobapi-key": "cc791b21-d5b0-4b71-b054-a1cd9e98e5ea",
    "User-Agent": "Aegean/1.1.8 (Android:Google Store; OS:15; Device:Google:Pixel-7; Library:okhttp/4.12.0)",
    "DeviceId": "231cf7e8-b701-3800-83b0-35cb04b1908f",
    "SessionId": "0114c1f0-c719-437f-a69a-91f83e18baa3",
    "Content-Type": "application/json; charset=UTF-8",
    "Host": "mobapi.aegeanair.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

def login_and_send_sms(username, password, phone):
    print(f"[+] Initializing login for: {username}")
    
    # Step 1: Auth with Password
    auth_payload = {
        "password": password,
        "username": username
    }
    params = {
        "lang": "en",
        "appVersion": "102",
        "origin": "app"
    }
    
    res = requests.post(f"{BASE_URL}/connect/auth/password", headers=HEADERS, json=auth_payload, params=params)
    
    if res.status_code != 200:
        print(f"[-] Login failed: {res.status_code}")
        print(res.text)
        return
    
    data = res.json()
    two_factor_token = data.get("twoFactorToken") # Note: Field name might vary based on real response
    
    if not two_factor_token:
        # Fallback: In some cases, the token might be in a nested 'data' object
        two_factor_token = data.get("data", {}).get("twoFactorToken")

    if not two_factor_token:
        print("[-] Could not extract twoFactorToken from response.")
        return

    print(f"[+] Success! Extracted Token: {two_factor_token[:30]}...")

    # Step 2: Send OTP
    print(f"[+] Requesting SMS OTP for: {phone}")
    sms_payload = {
        "channel": "sms",
        "language": "en",
        "to": phone,
        "twoFactorToken": two_factor_token
    }
    
    res_sms = requests.post(f"{BASE_URL}/connect/send-otp", headers=HEADERS, json=sms_payload, params=params)
    
    if res_sms.status_code == 200:
        print("[+] SMS Sent Successfully!")
        print(res_sms.text)
    elif res_sms.status_code == 429:
        print("[-] Rate Limited: Too Many Requests.")
        print(res_sms.json().get("data", {}).get("errorMessage"))
    else:
        print(f"[-] SMS Request failed: {res_sms.status_code}")
        print(res_sms.text)

if __name__ == "__main__":
    # Test Data from HAR
    USER = "deepanshusinghdigitalheroes@gmail.com"
    PASS = "Facebook@ds12,"
    PHONE = "+39 3515023566"
    
    login_and_send_sms(USER, PASS, PHONE)
