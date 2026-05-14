import requests
import json

def test_viyalite_flow():
    base_url = "https://api.salamyo.com"
    mobile = "+393519139022"
    
    # Step 1: Check Account
    print("Step 1: Checking Account Status...")
    check_url = f"{base_url}/auth/account/checkAccount"
    check_headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/4.9.2"
    }
    check_payload = {
        "request": {
            "mobile": mobile
        },
        "requestId": "187056824",
        "userEnv": {
            "appBuild": 453,
            "appId": "com.kinkey.vgolite",
            "appVersion": "1.2.6",
            "deviceId": "116158d944b4fe395afe34ee12a569a0764a436a"
        }
    }
    
    response = requests.post(check_url, headers=check_headers, json=check_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text.encode('utf-8')}")
    
    if response.status_code != 200:
        return

    # Step 2: Request SMS OTP
    # Note: This requires a valid captcha ticket from getCaptchaSetting which expires.
    # We use a placeholder or the one from the HAR for demonstration.
    print("\nStep 2: Requesting SMS OTP...")
    sms_url = f"{base_url}/auth/account/getAuthSms"
    sms_headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "okhttp/4.9.2"
    }
    sms_payload = {
        "request": {
            "captchaTicket": "{\"captchaValue\":\"9a2a0969-b1f3-4972-9352-532d7bf35fa2\",\"captchaType\":\"fallback\"}",
            "mobile": mobile
        },
        "requestId": "187056826",
        "userEnv": {
            "cola": "h8bJs/Uc1aFS8fCV...",
            "mouse": "wBJHgKGxCngZrLC2...",
            "signal": "{\"uuId\":\"W0O02byR...\"}"
        }
    }
    
    response = requests.post(sms_url, headers=sms_headers, json=sms_payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_viyalite_flow()
