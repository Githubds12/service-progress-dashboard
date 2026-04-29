import requests
import json
import uuid

class GooobetAPI:
    def __init__(self, phone):
        self.phone = phone
        self.base_url = "https://api.gooobet.com"
        self.session = requests.Session()
        self.app_guid = str(uuid.uuid4()).replace('-', '')[:16] + "_2"
        self.headers = {
            "User-Agent": "org.gooobet.client-user-agent/gooobet-v253.0.1",
            "Content-Type": "application/json; charset=UTF-8",
            "X-App-Id": "1793",
            "X-Whence": "22",
            "X-Referral": "253",
            "X-Language": "en_GB"
        }
        self.auth = None

    def get_captcha(self):
        url = f"{self.base_url}/captcha/v1/GetCaptcha"
        payload = {
            "AppGuid": self.app_guid,
            "Language": "en_GB",
            "Method": "Registration",
            "VersionGen": 2,
            "Login": ""
        }
        response = self.session.post(url, headers=self.headers, json=payload)
        return response.json()

    def register(self, captcha_id, hd_token):
        url = f"{self.base_url}/Account/v1.1/Mb/Register/Registration"
        payload = {
            "CaptchaId": captcha_id,
            "ImageText": hd_token,
            "Data": {
                "RegType": 2,
                "CountryId": 71,
                "CurrencyId": 99,
                "Phone": self.phone,
                "RulesConfirmation": 1,
                "SharePersonalDataConfirmation": 1,
                "TimeZone": "5.3"
            }
        }
        response = self.session.post(url, headers=self.headers, json=payload)
        res = response.json()
        if res.get("Success"):
            self.auth = res.get("Value", {}).get("Auth")
        return res

    def send_otp(self):
        if not self.auth:
            return {"Error": "Not registered yet"}
        url = f"{self.base_url}/Account/v1/SendCode"
        payload = {
            "Data": {},
            "Auth": {
                "Guid": self.auth["Guid"],
                "Token": self.auth["Token"]
            }
        }
        response = self.session.post(url, headers=self.headers, json=payload)
        res = response.json()
        if res.get("Success"):
            # Update token from response
            self.auth["Token"] = res.get("Value", {}).get("Auth", {}).get("Token")
        return res

    def verify_otp(self, code):
        if not self.auth:
            return {"Error": "Not registered yet"}
        url = f"{self.base_url}/Account/v1/CheckCode"
        payload = {
            "Data": {"Code": code},
            "Auth": {
                "Guid": self.auth["Guid"],
                "Token": self.auth["Token"]
            }
        }
        response = self.session.post(url, headers=self.headers, json=payload)
        return response.json()

if __name__ == "__main__":
    # Test phone number
    api = GooobetAPI("8319350528")
    
    print("[*] Getting Captcha...")
    captcha = api.get_captcha()
    print(f"[+] Captcha ID: {captcha.get('id')}")
    
    # Note: hd-api/verify payload generation is not implemented as it requires complex sensor data.
    # Replaying a token from HAR for demonstration of subsequent steps if possible, 
    # but normally this would fail in a real test without a fresh valid token.
    print("[!] HD-API token required for Registration. Automation feasibility is low.")
    
    # Placeholder for token
    hd_token = "REPLACE_WITH_VALID_HD_TOKEN"
    
    # Registration would go here
    # print("[*] Attempting Registration...")
    # reg = api.register(captcha.get('id'), hd_token)
    # print(reg)
