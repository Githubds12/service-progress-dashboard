import requests
import time
import re
import hashlib

# --- Configuration ---
IP = "62.238.2.204"
API_PORT = "8090"
TOKEN = "Scxfqcsgg"
BASE_URL = f"http://{IP}:{API_PORT}/api"

class FullyAutoMegogo:
    def __init__(self):
        self.session = requests.Session()
        self.did = "ANDROID3318301749__61fb946d2a357bd7"
        self.session.headers.update({
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 15; Google Pixel 7; Build/AP4A.250205.002)",
            "X-Client-Type": "Android",
            "X-Client-Version": "5.8.6",
            "Device-Name": "Google Pixel 7",
            "Device-Model": "Pixel 7",
            "Content-Type": "application/x-www-form-urlencoded"
        })
        self.phone_number = None

    def generate_sign(self, params):
        """Generates sign using key=value concatenation in alphabetical order."""
        # Pattern: action=senddid=...lang=enlogin=...remember=1
        sorted_keys = sorted(params.keys())
        base_string = "".join(f"{k}={params[k]}" for k in sorted_keys)
        md5_hex = hashlib.md5(base_string.encode()).hexdigest()
        return f"{md5_hex}_android_drm_22"

    def get_italy_number(self):
        url = f"{BASE_URL}/get_numbers"
        params = {"country": "IT", "operator": "iliad", "count": 1, "token": TOKEN}
        try:
            res = requests.get(url, params=params)
            data = res.json()
            if data.get("success") and data.get("number"):
                self.phone_number = data["number"][0]
                print(f"[+] Obtained Italy Number: {self.phone_number}")
                return True
        except: pass
        return False

    def trigger_otp(self):
        url = "https://api.megogo.net/v1/auth/phone"
        formatted_phone = f"+{self.phone_number}"
        
        # Exact params from the successful HAR log
        params = {
            "action": "send",
            "did": self.did,
            "lang": "en",
            "login": formatted_phone,
            "remember": "1"
        }
        params["sign"] = self.generate_sign(params)
        
        print(f"[*] Triggering Megogo OTP for {formatted_phone}...")
        try:
            res = self.session.post(url, data=params)
            data = res.json()
            if data.get("result") == "ok":
                print(f"[+] OTP Sent! {data['data']['status']['message']}")
                return True
            print(f"[-] Megogo Failed: {data}")
        except Exception as e:
            print(f"[-] Megogo Request Error: {e}")
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
                    match = re.search(r'\b(\d{4})\b', str(data)) # Megogo uses 4-digit codes
                    if match:
                        otp = match.group(1)
                        print(f"[+] Received OTP: {otp}")
                        return otp
                time.sleep(interval)
            except: pass
        return None

    def verify_otp(self, otp):
        url = "https://api.megogo.net/v1/auth/phone"
        formatted_phone = f"+{self.phone_number}"
        params = {
            "action": "verify",
            "did": self.did,
            "lang": "en",
            "login": formatted_phone,
            "remember": "1",
            "verification_code": otp
        }
        params["sign"] = self.generate_sign(params)
        try:
            res = self.session.post(url, data=params)
            data = res.json()
            if data.get("result") == "ok":
                print("[+] SUCCESS! Megogo Automation Completed.")
                return True
            print(f"[-] Final Step Failed: {data}")
        except Exception as e:
            print(f"[-] Final Step Error: {e}")
        return False

    def run_with_retries(self, max_attempts=10):
        for i in range(1, max_attempts + 1):
            print(f"\n--- ATTEMPT {i}/{max_attempts} ---")
            if self.get_italy_number():
                if self.trigger_otp():
                    otp = self.wait_for_otp()
                    if otp:
                        if self.verify_otp(otp):
                            return True
            time.sleep(10) # 10s cooldown to avoid rate limits
        return False

if __name__ == "__main__":
    FullyAutoMegogo().run_with_retries()
