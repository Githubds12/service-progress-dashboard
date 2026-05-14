import requests
import json

def test_pokerbet():
    session = requests.Session()
    phone = "+380635550123"
    form_id = "6329ae824a8a282e41d22024"
    
    # Step 0: Ping to get initial session/XSRF if needed
    url_ping = "https://tornbee.com/api/v2/ping/"
    print("[*] Pinging for initial state...")
    res_ping = session.post(url_ping)
    print(f"Ping Status: {res_ping.status_code}")
    
    # Step 1: Request OTP
    url_start = f"https://tornbee.com/api/v2/reg_forms/{form_id}/set_phone/"
    payload_start = {
        "phone": phone,
        "promo_code": "",
        "metadata": {"page": False, "attempt_index": 1}
    }
    
    print(f"[*] Requesting OTP for {phone}...")
    # Note: Might need to handle DataDome cookies here if blocked
    response_start = session.post(url_start, json=payload_start)
    print(f"Status: {response_start.status_code}")
    print(f"Response: {response_start.text}")
    
    if response_start.status_code == 200:
        print("[+] OTP Request Step (Simulated) Successful!")
    else:
        print("[-] Blocked or Failed.")

if __name__ == "__main__":
    test_pokerbet()
