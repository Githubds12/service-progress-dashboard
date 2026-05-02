import requests
import time
import re
from api import DerivAPI

# --- Configuration ---
IP = "62.238.2.204"
API_PORT = "8090"
TOKEN = "Scxfqcsgg"
BASE_URL = f"http://{IP}:{API_PORT}/api"

class FullyAutoDeriv:
    def __init__(self):
        self.api = DerivAPI()
        self.phone_number = None
        self.session_token = "ory_st_FanbtKIBenZzcCtbpx8KUTvFjw52pnUb" # Placeholder from HAR

    def get_number(self):
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

    def trigger_otp(self):
        print(f"[*] Fetching login flow...")
        flow = self.api.get_login_flow()
        flow_id = flow.get('id')
        if not flow_id:
            print("[-] Failed to get flow ID")
            return False
            
        formatted_phone = f"+{self.phone_number}"
        print(f"[*] Requesting OTP for {formatted_phone}...")
        res = self.api.request_phone_verification(flow_id, formatted_phone, self.session_token)
        
        # Ory returns 400 when it sends the code and expects entry
        if 'A code was sent' in str(res):
            print(f"[+] OTP Sent successfully!")
            return flow_id
        else:
            print(f"[-] Trigger Failed: {res}")
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
                    # Deriv uses 6-digit codes
                    match = re.search(r'\b(\d{6})\b', str(data))
                    if match:
                        otp = match.group(1)
                        print(f"[+] Received OTP: {otp}")
                        return otp
                time.sleep(interval)
            except: pass
        return None

    def verify_otp(self, flow_id, otp):
        formatted_phone = f"+{self.phone_number}"
        print(f"[*] Submitting OTP {otp}...")
        res = self.api.submit_otp(flow_id, formatted_phone, otp, self.session_token)
        
        if res.get('status') == 'success' or 'invalid' not in str(res):
            print("[+] SUCCESS! Deriv Automation Completed.")
            return True
        else:
            print(f"[-] Verification Failed: {res}")
            return False

    def run(self):
        if self.get_number():
            flow_id = self.trigger_otp()
            if flow_id:
                otp = self.wait_for_otp()
                if otp:
                    self.verify_otp(flow_id, otp)

if __name__ == "__main__":
    FullyAutoDeriv().run()
