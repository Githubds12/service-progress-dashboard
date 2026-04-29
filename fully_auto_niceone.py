import time
import requests
import uuid
import random

# --- Configuration ---
IP = "62.238.2.204"
API_PORT = "8090"
TOKEN = "Scxfqcsgg"
BASE_URL = f"http://{IP}:{API_PORT}/api"

class FullyAutoNiceOne:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "NiceOne/10.5.4 (com.NiceOne.App; build:40344; Android 15)",
            "x-oc-merchant-id": "1",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Requested-With": "com.NiceOne.App"
        }
        self.phone_number = None

    def get_number(self, country="SA"):
        # NiceOne is Saudi based, but let's try Italy as well if requested
        url = f"{BASE_URL}/get_numbers"
        params = {"country": country, "count": 1, "token": TOKEN}
        try:
            res = requests.get(url, params=params)
            data = res.json()
            if data.get("success") and data.get("number"):
                self.phone_number = data["number"][0]
                print(f"[+] Obtained Number: {self.phone_number}")
                return True
        except: pass
        return False

    def init_session(self):
        print("[*] Initializing NiceOne Session...")
        url = "https://api.niceonesa.com/?route=feed/rest_api/session"
        try:
            res = self.session.get(url, headers=self.headers)
            # The session ID is in the cookies
            sess_id = self.session.cookies.get("PHPSESSID")
            if sess_id:
                self.headers["x-oc-session"] = sess_id
                print(f"[+] Session Initialized: {sess_id}")
                return True
        except Exception as e:
            print(f"[-] Session Init Failed: {e}")
        return False

    def trigger_otp(self, first_name="Tester"):
        # Ensure number has + prefix for NiceOne
        phone = self.phone_number if self.phone_number.startswith("+") else f"+{self.phone_number}"
        url = "https://api.niceonesa.com/?route=rest/register/register_v2"
        payload = {
            "firstname": first_name,
            "telephone": phone
        }
        print(f"[*] Triggering NiceOne OTP for {phone}...")
        try:
            res = self.session.post(url, json=payload, headers=self.headers)
            data = res.json()
            if data.get("success") == 1 or "step" in data:
                print(f"[+] NiceOne OTP Triggered. Step: {data.get('step')}")
                return True
            print(f"[-] Trigger Failed: {data.get('error', data)}")
        except Exception as e:
            print(f"[-] Trigger Error: {e}")
        return False

    def poll_for_sms(self, timeout=120):
        print(f"[*] Polling for SMS on {self.phone_number}...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            url = f"{BASE_URL}/get_sms"
            params = {"number": self.phone_number, "token": TOKEN}
            try:
                res = requests.get(url, params=params)
                data = res.json()
                if data.get("success") and data.get("sms"):
                    sms_text = data["sms"][0]
                    code = "".join(filter(str.isdigit, sms_text))
                    if len(code) >= 4:
                        print(f"[+] Received OTP: {code}")
                        return code
            except: pass
            time.sleep(10)
        print("[-] SMS Polling Timeout.")
        return None

    def verify_otp(self, code):
        url = "https://api.niceonesa.com/?route=rest/register/verifyphone_v2"
        payload = {"code": code}
        print(f"[*] Verifying OTP {code}...")
        try:
            res = self.session.post(url, json=payload, headers=self.headers)
            data = res.json()
            if data.get("success") == 1:
                print("[+] NiceOne Registration Successful!")
                return True
            print(f"[-] Verification Failed: {data.get('error', data)}")
        except Exception as e:
            print(f"[-] Verification Error: {e}")
        return False

    def run_flow(self, country="SA"):
        if self.init_session():
            if self.get_number(country):
                if self.trigger_otp():
                    code = self.poll_for_sms()
                    if code:
                        return self.verify_otp(code)
        return False

if __name__ == "__main__":
    # Test with Saudi number as per original HAR
    FullyAutoNiceOne().run_flow(country="SA")
