import requests
import json
import time

class TbankAPI:
    def __init__(self, phone):
        self.phone = phone
        self.session = requests.Session()
        self.base_url = "https://id.tbank.ru/auth"
        self.cid = None
        self.token = None
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "mbsme-android/3.23 (Android 15; google Pixel 7)",
            "X-Lang": "ru",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "id.tbank.ru",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

    def authorize(self):
        url = f"{self.base_url}/authorize"
        params = {
            "cpswc": "true",
            "ccc": "true"
        }
        payload = {
            "client_id": "mbsme",
            "redirect_uri": "mobile://",
            "response_type": "code",
            "response_mode": "json",
            "display": "json",
            "device_id": "653b5540d1afe722",
            "client_version": "14.0.2-hotfix1",
            "vendor": "tinkoff_android",
            "claims": json.dumps({"id_token": {"nickname": None, "email": None, "email_verified": None}})
        }
        
        print(f"[*] Initializing Authorization...")
        response = self.session.post(url, params=params, data=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.cid = data.get('cid')
            print(f"[+] CID obtained: {self.cid}")
            return True
        else:
            print(f"[-] Authorization failed: {response.status_code}")
            print(response.text)
            return False

    def send_sms(self):
        if not self.cid:
            return False
            
        url = f"{self.base_url}/step"
        params = {
            "cid": self.cid,
            "cpswc": "true",
            "ccc": "true"
        }
        
        fingerprint = {
            "appVersion": "3.23",
            "clientLanguage": "ru",
            "clientTimezone": -330,
            "timeZoneName": "Asia/Kolkata",
            "latitude": None,
            "longitude": None,
            "mobileDeviceModel": "Google Pixel 7",
            "mobileDeviceOs": "Android",
            "mobileDeviceOsVersion": "15",
            "userAgent": "mbsme-android/3.23 (Android 15; google Pixel 7)",
            "mobileDeviceId": "653b5540d1afe722",
            "tDeviceId": "653b5540d1afe722",
            "connectionType": "WiFi",
            "bundleId": "ru.tinkoff.sme",
            "locale": "ru"
        }
        
        payload = {
            "phone": self.phone,
            "fingerprint": json.dumps(fingerprint),
            "step": "phone"
        }
        
        print(f"[*] Sending SMS to {self.phone}...")
        response = self.session.post(url, params=params, data=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('token')
            print(f"[+] SMS sent. Step Token: {self.token}")
            return True
        else:
            print(f"[-] SMS sending failed: {response.status_code}")
            print(response.text)
            return False

    def verify_otp(self, otp):
        if not self.cid or not self.token:
            return False
            
        url = f"{self.base_url}/step"
        params = {
            "cid": self.cid,
            "cpswc": "true",
            "ccc": "true"
        }
        
        payload = {
            "otp": otp,
            "token": self.token,
            "step": "otp"
        }
        
        print(f"[*] Verifying OTP: {otp}...")
        response = self.session.post(url, params=params, data=payload, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                print(f"[-] Verification Error: {data.get('error_message')}")
            else:
                print(f"[+] Verification Successful!")
                print(json.dumps(data, indent=2))
            return True
        else:
            print(f"[-] OTP verification failed: {response.status_code}")
            print(response.text)
            return False

if __name__ == "__main__":
    # Test credentials from HAR
    test_phone = "+393517641332"
    api = TbankAPI(test_phone)
    
    if api.authorize():
        time.sleep(1)
        if api.send_sms():
            print("\n[!] Manual Input Required: Check SMS for code.")
            # In a real automation context, we'd wait for the code or use a placeholder
            api.verify_otp("1234") # Dummy test
