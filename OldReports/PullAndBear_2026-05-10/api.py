import requests
import json

def test_pullandbear_flow():
    # Base URL and headers
    base_url = "https://www.pullandbear.com/itxrest/2/user/store/28009400"
    headers = {
        "User-Agent": "PullAndBear_eCom/2604.1.0 (Pixel 7; Android; 15; en-IN; ITXCORE 1)",
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json"
    }
    
    # 1. SMS Request
    print("[*] Requesting SMS OTP...")
    sms_url = f"{base_url}/account-validation-code?appId=4&languageId=-1&catalogId=20309455"
    sms_payload = {
        "logon": "+393720514818",
        "option": "OTP-SMS"
    }
    
    try:
        res_sms = requests.post(sms_url, headers=headers, json=sms_payload, timeout=10)
        print(f"SMS Request Status: {res_sms.status_code}")
        print(f"Response: {res_sms.text[:200]}")
    except Exception as e:
        print(f"SMS Request Failed: {e}")

    # 2. OTP Submission (Login)
    # Note: Requires a valid OTP and a password
    print("\n[*] Submitting OTP (Simulated)...")
    login_url = f"{base_url}/phone-logon?appId=4&languageId=-1&catalogId=20309455"
    login_payload = {
        "phone": {
            "countryCode": "+39",
            "subscriberNumber": "3720514818"
        },
        "code": "252525",
        "password": "Password123!"
    }
    
    try:
        res_login = requests.post(login_url, headers=headers, json=login_payload, timeout=10)
        print(f"OTP Submit Status: {res_login.status_code}")
        print(f"Response: {res_login.text[:200]}")
    except Exception as e:
        print(f"OTP Submit Failed: {e}")

if __name__ == "__main__":
    test_pullandbear_flow()
