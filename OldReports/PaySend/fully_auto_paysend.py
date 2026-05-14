import time
import json
import re
import uuid
import random

try:
    from curl_cffi import requests
    HAS_CURL_CFFI = True
except ImportError:
    import requests
    HAS_CURL_CFFI = False

# --- Configuration ---
IP = "62.238.2.204"
API_PORT = "8090"
TOKEN = "Scxfqcsgg"
BASE_URL = f"http://{IP}:{API_PORT}/api"

class FullyAutoPaySend:
    def __init__(self):
        self.session = requests.Session()
        self.impersonate = "chrome110" if HAS_CURL_CFFI else None
        self.phone_number = None

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

    def trigger_paysend_otp(self):
        sec_uuid = uuid.uuid4().hex[:16]
        device_id = f"84-{random.randint(100000000000000, 999999999999999)}"
        
        # CRITICAL FIX: Match X-Phone-Country to the actual phone number (39 for Italy)
        country_code = "39" if self.phone_number.startswith("39") else "380"
        
        headers = {
            "User-Agent": "okhttp/4.12.0",
            "Content-Type": "application/xml",
            "X-Phone-Country": country_code, # SYNCED
            "Client-Software": "Android v4.9.10",
            "auth_type": "ANONYMOUS",
            "sec_uuid": sec_uuid,
            "store": "google",
            "XML_REQUEST_ID": str(uuid.uuid4())
        }

        kwargs = {"headers": headers}
        if HAS_CURL_CFFI:
            kwargs["impersonate"] = self.impersonate

        xml_url = "https://api.paysend.com/api/xml.jsp"
        
        # Human speed pre-checks
        print("[*] Velocity Check 1...")
        check_xml = f"""<request><auth><client_software>Android v4.9.10</client_software><id>{device_id}</id><lang>en</lang><store>google</store><auth_type>ANONYMOUS</auth_type><sec_uuid>{sec_uuid}</sec_uuid></auth><extra name="phone">{self.phone_number}</extra><request_type>is_user_registered</request_type></request>"""
        self.session.post(xml_url, data=check_xml, **kwargs)
        time.sleep(5.0)
        
        print("[*] Velocity Check 2...")
        fields_xml = f"""<request><auth><client_software>Android v4.9.10</client_software><id>{device_id}</id><lang>en</lang><store>google</store><auth_type>ANONYMOUS</auth_type><sec_uuid>{sec_uuid}</sec_uuid></auth><extra name="phone">{self.phone_number}</extra><request_type>get_registration_fields</request_type></request>"""
        self.session.post(xml_url, data=fields_xml, **kwargs)
        time.sleep(5.0)

        # Final Registration
        reg_url = "https://api.paysend.com/api/json/registration"
        payload = {
            "client_id": "PAYSEND_MOBILE_APP",
            "secret": "12345678",
            "phone": self.phone_number,
            "email": f"tester_{uuid.uuid4().hex[:6]}@gmail.com",
            "marketing_opt_in": "0"
        }
        
        json_headers = headers.copy()
        json_headers["Content-Type"] = "application/json; charset=utf-8"
        json_kwargs = {"headers": json_headers}
        if HAS_CURL_CFFI:
            json_kwargs["impersonate"] = self.impersonate

        print(f"[*] Submitting Native Registration (Country Sync: {country_code})...")
        try:
            res = self.session.post(reg_url, json=payload, **json_kwargs)
            data = res.json()
            if "balId" in data:
                print(f"[+] PaySend OTP Triggered Successfully! balId: {data['balId']}")
                return True
            print(f"[-] PaySend Trigger Failed (Code {data.get('code')}): {data.get('message', data)}")
        except Exception as e:
            print(f"[-] PaySend Request Error: {e}")
        return False

    def run_with_retries(self, max_attempts=10):
        for i in range(1, max_attempts + 1):
            print(f"\n--- ATTEMPT {i}/{max_attempts} ---")
            if self.get_italy_number():
                if self.trigger_paysend_otp():
                    return True
            print("[*] Cooling down for 15s...")
            time.sleep(15)
        return False

if __name__ == "__main__":
    FullyAutoPaySend().run_with_retries()
