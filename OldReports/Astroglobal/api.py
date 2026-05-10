import requests
import json

def test_astroglobal_flow():
    base_url = "https://api.astroglobal.com"
    
    # Step 1: Check User (Triggers SMS)
    print("Step 1: Check User (Requesting OTP)...")
    url = f"{base_url}/account/check-user/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "okhttp/4.9.2"
    }
    payload = {
        "phone": "7456821389",
        "sign_up_method": "STANDARD"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\nOTP Request successful (Service returned user registration status).")
    else:
        print("\nOTP Request failed.")

if __name__ == "__main__":
    test_astroglobal_flow()
