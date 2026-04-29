import time
import json
import re
import requests

# --- Configuration ---
IP = "62.238.2.204"
API_PORT = "8090"
TOKEN = "Scxfqcsgg"
BASE_URL = f"http://{IP}:{API_PORT}/api"

class FullyAutoIBISmart:
    def __init__(self):
        self.session = requests.Session()
        self.phone_number = None
        # Exact API Key from HAR
        self.api_key = "msdjfo@%#T^YrgsrfSFDHnmblpfsjbfsnk;ml358ueoj5%Y#Y%#yhfb#%@#$^T@4nt436hdgjmdhfmg"

    def get_italy_number(self):
        url = f"{BASE_URL}/get_numbers"
        params = {"country": "IT", "operator": "iliad", "count": 1, "token": TOKEN}
        try:
            res = requests.get(url, params=params)
            data = res.json()
            if data.get("success") and data.get("number"):
                self.phone_number = data["number"][0]
                print(f"[+] Obtained Number: {self.phone_number}")
                return True
        except: pass
        return False

    def trigger_ibismart_otp(self):
        # IBI Smart usually expects Israeli numbers (05x). 
        # We will try the Italian number in full format first.
        url = "https://smartapi.ibi.co.il/api/onboarding/otp/start"
        headers = {
            "api-key": self.api_key,
            "User-Agent": "Android + 3.1.9",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "smartapi.ibi.co.il",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        
        # Test with + prefix
        formatted_phone = f"+{self.phone_number}" if not self.phone_number.startswith("+") else self.phone_number
        payload = {"isVoice": False, "phone": formatted_phone}
        
        print(f"[*] Triggering IBI Smart OTP for {formatted_phone}...")
        try:
            res = self.session.post(url, json=payload, headers=headers)
            data = res.json()
            if data.get("success"):
                print("[+] IBI Smart OTP Triggered!")
                return True
            
            # If failed, retry without + prefix (Some gateways are picky)
            print("[*] Retrying without '+' prefix...")
            payload["phone"] = self.phone_number.replace("+", "")
            res = self.session.post(url, json=payload, headers=headers)
            data = res.json()
            if data.get("success"):
                print("[+] IBI Smart OTP Triggered (No +)!")
                return True
                
            print(f"[-] Trigger Failed: {res.text}")
        except Exception as e:
            print(f"[-] Request Error: {e}")
        return False

    def wait_for_otp(self, timeout=60, interval=5):
        url = f"{BASE_URL}/get_messages"
        params = {"token": TOKEN, "number": self.phone_number}
        print(f"[*] Polling for SMS on {self.phone_number}...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                res = requests.get(url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    # IBI Smart OTP is usually 6 digits
                    match = re.search(r'\b(\d{6})\b', str(data))
                    if match:
                        otp = match.group(1)
                        print(f"[+] Received OTP: {otp}")
                        return otp
                time.sleep(interval)
            except: pass
        return None

    def verify_ibismart_otp(self, otp):
        print(f"[*] Verifying IBI Smart OTP {otp}...")
        url = "https://smartapi.ibi.co.il/api/onboarding/otp/validate"
        headers = {
            "api-key": self.api_key,
            "User-Agent": "Android + 3.1.9",
            "Content-Type": "application/json; charset=UTF-8"
        }
        payload = {
            "code": str(otp),
            "phone": self.phone_number,
            "utm_source": "app"
        }
        try:
            res = self.session.post(url, json=payload, headers=headers)
            data = res.json()
            if data.get("success"):
                print("[+] SUCCESS! IBI Smart Registration Complete.")
                return True
            print(f"[-] Verification Failed: {res.text}")
        except: pass
        return False

    def run_with_retries(self, max_attempts=10):
        for i in range(1, max_attempts + 1):
            print(f"\n--- ATTEMPT {i}/{max_attempts} ---")
            if self.get_italy_number():
                if self.trigger_ibismart_otp():
                    otp = self.wait_for_otp()
                    if otp:
                        if self.verify_ibismart_otp(otp):
                            return True
            print("[*] Cooling down for 10s...")
            time.sleep(10)
        return False

if __name__ == "__main__":
    FullyAutoIBISmart().run_with_retries()
