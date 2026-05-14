import requests
import json
import uuid

def test_bolt_food():
    session = requests.Session()
    phone = "+918791267460"
    phone_uuid = str(uuid.uuid4())
    
    # Step 1: Start verification
    url_start = "https://deliveryuser.live.boltsvc.net/profile/verification/start"
    params = {
        "version": "FA.1.108",
        "language": "en-US",
        "channel": "googleplay",
        "deviceId": "00b4394f2955a32f"
    }
    payload_start = {
        "phone_number": phone,
        "phone_uuid": phone_uuid,
        "type": "phone",
        "last_known_state": {}
    }
    
    print(f"[*] Requesting OTP for {phone}...")
    response_start = session.post(url_start, params=params, json=payload_start)
    print(f"Status: {response_start.status_code}")
    print(f"Response: {response_start.text}")
    
    if response_start.status_code == 200:
        print("[+] OTP Request Successful!")
    else:
        print("[-] OTP Request Failed.")

if __name__ == "__main__":
    test_bolt_food()
