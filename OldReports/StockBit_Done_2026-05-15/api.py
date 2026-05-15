import requests
import json

# Target: StockBit (com.stockbit.android)
# Backend: Exodus API
BASE_URL = "https://exodus.stockbit.com"

def check_email(email):
    print(f"[*] Checking email: {email}")
    url = f"{BASE_URL}/registration/v3/check/email"
    payload = {
        "email": email,
        "key": "",
        "type": 1
    }
    res = requests.post(url, json=payload)
    print(f"[-] Response: {res.text}")
    return res.json().get("data", {}).get("key")

def verify_email_otp(key, otp):
    print(f"[*] Verifying email OTP: {otp}")
    url = f"{BASE_URL}/registration/v3/otp/email"
    payload = {
        "key": key,
        "otp": otp
    }
    res = requests.post(url, json=payload)
    print(f"[-] Response: {res.text}")
    return res.json().get("data", {}).get("valid")

def check_phone(key, phone):
    print(f"[*] Checking phone: {phone}")
    url = f"{BASE_URL}/registration/v3/check/phone"
    payload = {
        "channel": "CHANNEL_SMS",
        "code": "39", # Italy code from HAR
        "key": key,
        "phone": phone
    }
    res = requests.post(url, json=payload)
    print(f"[-] Response: {res.text}")
    return res.json().get("data", {}).get("valid")

def verify_phone_otp(key, otp):
    print(f"[*] Verifying phone OTP: {otp}")
    url = f"{BASE_URL}/registration/v3/otp/phone"
    payload = {
        "key": key,
        "otp": otp,
        "player_id": "80468e4b037310fb64516bb894a5be9ffb59940dad3cd8f2ce7a1be1297ceacf",
        "pushnotif_id": "80468e4b037310fb64516bb894a5be9ffb59940dad3cd8f2ce7a1be1297ceacf"
    }
    res = requests.post(url, json=payload)
    print(f"[-] Response: {res.text}")
    return res.json()

if __name__ == "__main__":
    # Test values (Sample)
    email = "test_recon@digitalheroes.com"
    key = check_email(email)
    if key:
        print("[+] Success: Key received.")
