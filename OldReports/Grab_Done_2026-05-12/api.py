import requests
import json
import time

class GrabAPI:
    def __init__(self, phone, country_code="IT"):
        self.phone = phone
        self.country_code = country_code
        self.session = requests.Session()
        self.base_url = "https://api.grab.com/grabid/v1"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Grab/5.408.0 (Android 15; Pixel 7)",
            "Host": "api.grab.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        self.device_id = "3346dff226996b4a"
        self.challenge_session_id = None

    def init_challenge(self):
        url = f"{self.base_url}/challengesession/challengeSession"
        params = {
            "isIncludeCurrentGeneratedChallenge": "true"
        }
        print("[*] Initializing Challenge Session...")
        response = self.session.get(url, params=params, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.challenge_session_id = data.get("challengeSessionID")
            print(f"[+] Challenge Session ID: {self.challenge_session_id}")
            return True
        else:
            print(f"[-] Failed to init challenge: {response.status_code}")
            return False

    def send_otp(self):
        if not self.challenge_session_id:
            print("[-] No challenge session ID. Solve Arkose first.")
            return False
            
        url = f"{self.base_url}/phone/otp"
        payload = {
            "method": "SMS",
            "countryCode": self.country_code,
            "phoneNumber": self.phone,
            "templateID": "pax_android_production",
            "numDigits": 6,
            "deviceID": self.device_id,
            "deviceManufacturer": "Google",
            "deviceModel": "Pixel 7",
            "locale": "en_IN",
            "scenario": "signup"
        }
        
        # Note: In a real scenario, we'd need to have verified the ARKOSE challenge 
        # for this challengeSessionID before the server allows sending OTP.
        
        print(f"[*] Requesting OTP for {self.phone}...")
        response = self.session.post(url, json=payload, headers=self.headers)
        
        if response.status_code == 200:
            print("[+] OTP Request successful!")
            return True
        else:
            print(f"[-] OTP Request failed: {response.status_code}")
            print(response.text)
            return False

if __name__ == "__main__":
    # Test credentials from HAR
    test_phone = "393720513142"
    api = GrabAPI(test_phone)
    if api.init_challenge():
        print("[!] Note: Arkose Labs Captcha must be solved manually or via service.")
        # api.send_otp() # This will likely fail without verified challenge
