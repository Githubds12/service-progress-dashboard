import requests
import json
import uuid

def send_otp(phone, dial_code="+966"):
    url = "https://api.thechefz.co/v9/user/auth"
    headers = {
        "App-Version": "10.80.0",
        "Accept": "application/json",
        "User-Agent": "The Chefz/10.80.0 (com.nextwo.the_chefz;build:375;Android 15)",
        "UDID": str(uuid.uuid4())[:16].replace("-", ""),
        "City": "1",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "phone": phone,
        "dialCode": dial_code,
        "marketingMessagesAccepted": False,
        "userType": "1"
    }
    
    print(f"[*] Sending OTP request for {dial_code}{phone}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Response: {response.text}")
        return response.json()
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

if __name__ == "__main__":
    # Test with a sample number (from the HAR: 572302775)
    send_otp("572302775")
