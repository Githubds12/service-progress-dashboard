import requests
import json
import uuid

def test_amo_automation():
    print("Starting AMO Automation Test...")
    
    # 1. SMS Request
    # Note: Using the static sign from HAR for testing. 
    # Real automation would require reversing the signing algorithm.
    url_sms = "https://api.chatie.love/api/polaris/login-reg-sms-v2"
    params_sms = {
        "countryCode": "39",
        "sign": "4be7a6bc18d866a986f8e1ceeec68cc4bce6d5e5", # From HAR
        "cellphone": "3517085288"
    }
    
    headers = {
        "App-Key": "111001",
        "Platform": "android",
        "User-Agent": "Right-Android/2.30.0 default (Google, Pixel 7, 15; 35)",
        "Version-Name": "2.30.0",
        "Version-Code": "2511",
        "Yanhong-Channel": "polaris",
        "Host": "api.chatie.love",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    print(f"\nSending SMS Request for phone: {params_sms['cellphone']}")
    try:
        response_sms = requests.get(url_sms, params=params_sms, headers=headers)
        print(f"Status Code: {response_sms.status_code}")
        print(f"Response: {response_sms.text}")
        
        if response_sms.status_code == 200:
            data = response_sms.json()
            if data.get("code") == "000000":
                print("\nSuccessfully triggered SMS (or sign still valid).")
            else:
                print(f"\nServer returned error code: {data.get('code')}")
                if "sign" in response_sms.text.lower():
                    print("This likely indicates the 'sign' parameter is invalid or expired.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_amo_automation()
