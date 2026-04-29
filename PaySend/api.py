import requests
import json
import uuid

def test_paysend_automation():
    print("Starting PaySend Automation Test...")
    
    # 1. Initialization (Registration)
    url_reg = "https://api.paysend.com/api/json/registration"
    
    # Generate a random sec_uuid if needed, but using the one from HAR for stability
    sec_uuid = "a6e33d486bfb5b2e" 
    
    headers = {
        "auth_type": "ANONYMOUS",
        "Client-Software": "Android v4.9.10",
        "sec_uuid": sec_uuid,
        "store": "google",
        "XML_REQUEST_ID": str(uuid.uuid4()),
        "X-Phone-Country": "380", # From HAR
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "okhttp/4.12.0",
        "Host": "api.paysend.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    
    # Using the phone number from HAR
    phone = "393519566477" 
    email = f"test_{uuid.uuid4().hex[:8]}@gmail.com"
    
    payload_reg = {
        "client_id": "PAYSEND_MOBILE_APP",
        "secret": "12345678",
        "phone": phone,
        "email": email,
        "marketing_opt_in": "0"
    }
    
    print(f"\nSending Registration Request for phone: {phone}")
    response_reg = requests.post(url_reg, json=payload_reg, headers=headers)
    print(f"Status Code: {response_reg.status_code}")
    print(f"Response: {response_reg.text}")
    
    if response_reg.status_code == 200:
        data = response_reg.json()
        bal_id = data.get("balId")
        auth_key = data.get("authKey")
        
        if bal_id and auth_key:
            print("\nSuccessfully obtained balId and authKey.")
            # ... rest of the flow ...
        else:
            print("\nResponse received but no balId/authKey found. Might be already registered or rate limited.")
            if data.get("message"):
                print(f"Server Message: {data.get('message')}")
    else:
        print(f"\nRegistration request failed with status {response_reg.status_code}")

if __name__ == "__main__":
    test_paysend_automation()
