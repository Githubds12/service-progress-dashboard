import requests
import json

def test_coinstore_auth():
    session = requests.Session()
    phone = "1012345678"
    country_code = "+82"
    
    # Common Headers
    headers = {
        "User-Agent": "okhttp/4.10.0",
        "Content-Type": "application/json; charset=utf-8",
        "Host": "api.coinstore.com",
        "Connection": "Keep-Alive"
    }

    # Note: This test will fail without a valid session cookie and captcha token.
    # The purpose is to demonstrate the endpoint structure.

    # Step 1: Send SMS Gateway
    url_sms = "https://api.coinstore.com/v2/user/common/gateway/send/sms"
    sms_payload = {
        "countryCode": country_code,
        "mobile": phone,
        "scene": "6",
        "token": "" # This requires a GeeTest validate token
    }
    
    print(f"[*] Requesting SMS for {country_code}{phone} (Binding flow)...")
    try:
        res_sms = session.post(url_sms, headers=headers, json=sms_payload)
        print(f"Status: {res_sms.status_code}")
        print(f"Response: {res_sms.text}")
    except Exception as e:
        print(f"[-] Request failed: {e}")

    # Step 2: Binding Save
    url_bind = "https://api.coinstore.com/v2/user/mobile/binding/save"
    bind_payload = {
        "countryCode": country_code,
        "mobile": phone,
        "googleValidCode": "",
        "scene": "6",
        "mobileValidCode": "123456"
    }
    
    print(f"[*] Attempting to bind phone {phone} with code 123456...")
    try:
        res_bind = session.post(url_bind, headers=headers, json=bind_payload)
        print(f"Status: {res_bind.status_code}")
        print(f"Response: {res_bind.text}")
    except Exception as e:
        print(f"[-] Request failed: {e}")

if __name__ == "__main__":
    test_coinstore_auth()
