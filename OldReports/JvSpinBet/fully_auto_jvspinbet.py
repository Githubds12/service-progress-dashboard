import requests
import time
import re

# --- Configuration ---
IP = "62.238.2.204"
API_PORT = "8090"
TOKEN = "Scxfqcsgg"
BASE_URL = f"http://{IP}:{API_PORT}/api"

class FullyAutoJvSpinBet:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "org.jvspinbet.client-user-agent/jvspinbet-v253.0.1",
            "X-BundleId": "org.jvspinbet.client",
            "Version": "jvspinbet-v253.0.1",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "andind2022.com"
        }
        self.phone_number = None
        self.auth_data = {}

    def get_number(self, country="IN"):
        url = f"{BASE_URL}/get_numbers"
        params = {"country": country, "count": 1, "token": TOKEN}
        try:
            res = requests.get(url, params=params)
            data = res.json()
            if data.get("success") and data.get("number"):
                # JvSpinBet expects number without + or country code prefix in some fields, 
                # but let's see the HAR: "Phone":"7990158524" (India 91 prefix was in query but not body)
                # Actually HAR query had: phone=917990158524
                # Body had: "Phone":"7990158524"
                raw_number = data["number"][0]
                self.phone_number = raw_number
                print(f"[+] Obtained Number: {self.phone_number}")
                return True
        except: pass
        return False

    def get_captcha(self):
        # Registration requires a captcha. This is a blocker for full automation 
        # unless an OCR or manual solve is integrated.
        print("[!] Manual Captcha required for registration.")
        # In a real automated environment, we would use a captcha solving service.
        # For now, we simulate the structure.
        return "manual_solve_required"

    def trigger_registration_and_otp(self):
        url = "https://andind2022.com/Account/v1.1/Mb/Register/Registration"
        # Extract last 10 digits for India or relevant digits for the service
        short_phone = self.phone_number[-10:] if len(self.phone_number) > 10 else self.phone_number
        
        # Note: In a real run, CaptchaId and ImageText would be obtained from /GetCaptcha
        payload = {
            "CaptchaId": "65f82c04-615e-42d6-8820-f071bd3c97a0", # Placeholder
            "ImageText": "manual", # Placeholder
            "Data": {
                "RegType": 2,
                "CountryId": 71, # India
                "CurrencyId": 99, # INR
                "Phone": short_phone,
                "Birthday": "1998-05-05",
                "RulesConfirmation": 1,
                "SharePersonalDataConfirmation": 1
            }
        }
        print(f"[*] Attempting JvSpinBet Registration for {short_phone}...")
        try:
            res = self.session.post(url, json=payload, headers=self.headers)
            data = res.json()
            if data.get("Success"):
                self.auth_data = data["Value"]["Auth"]
                print(f"[+] Registration Initiated. Guid: {self.auth_data['Guid']}")
                
                # Now trigger the actual SMS send
                print("[*] Triggering SMS SendCode...")
                send_url = "https://andind2022.com/Account/v1/SendCode"
                send_payload = {
                    "Data": {},
                    "Auth": {
                        "Guid": self.auth_data["Guid"],
                        "Token": self.auth_data["Token"]
                    }
                }
                res_send = self.session.post(send_url, json=send_payload, headers=self.headers)
                send_data = res_send.json()
                if send_data.get("Success"):
                    self.auth_data["Token"] = send_data["Value"]["Auth"]["Token"]
                    print("[+] SMS Sent successfully!")
                    return True
            print(f"[-] Registration/OTP Trigger Failed: {data}")
        except Exception as e:
            print(f"[-] Error: {e}")
        return False

    def wait_for_otp(self, timeout=120):
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
                    # JvSpin codes are typically 6 digits
                    match = re.search(r'\b(\d{6})\b', sms_text)
                    if match:
                        code = match.group(1)
                        print(f"[+] Received OTP: {code}")
                        return code
            except: pass
            time.sleep(10)
        return None

    def verify_otp(self, code):
        url = "https://andind2022.com/Account/v1/CheckCode"
        payload = {
            "Data": {"Code": code},
            "Auth": {
                "Guid": self.auth_data["Guid"],
                "Token": self.auth_data["Token"]
            }
        }
        print(f"[*] Verifying OTP {code}...")
        try:
            res = self.session.post(url, json=payload, headers=self.headers)
            data = res.json()
            if data.get("Success"):
                print("[+] JvSpinBet Verification Successful!")
                return True
            print(f"[-] Verification Failed: {data}")
        except Exception as e:
            print(f"[-] Verification Error: {e}")
        return False

    def run_flow(self):
        if self.get_number(country="IN"):
            # Note: This will likely fail without a valid captcha solver
            if self.trigger_registration_and_otp():
                code = self.wait_for_otp()
                if code:
                    return self.verify_otp(code)
        return False

if __name__ == "__main__":
    FullyAutoJvSpinBet().run_flow()
