import requests
import json
import time

def send_otp(phone):
    url = "https://api.bnxdw4a.com/app/sendPhoneMsg"
    headers = {
        "Content-type": "application/json",
        "X-Requested-With": "poker21.fairplaycard.royalclub",
        "Origin": "https://www.bg678s.com",
        "Referer": "https://www.bg678s.com/"
    }
    # Note: These are static encrypted payloads from the HAR for demonstration of the endpoint existence
    # Real automation would require reversing the 'data' and 'sign' logic
    payload = {
        "data": "FD5ACE5FBAAEFF8E1A44EA30CE48D80760F76D42C8221730DCCB33944DE9E157DA5A01DE01B55F41EA10DD9CBE4B031C",
        "sign": "4d961c5ad3b0239e534f86215a39d14c",
        "dateTime": str(int(time.time() * 1000))
    }
    
    print(f"[*] Sending encrypted OTP request to {url}...")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Response: {response.text}")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    send_otp("919999999999")
