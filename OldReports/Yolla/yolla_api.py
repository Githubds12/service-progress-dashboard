import requests
import time

class YollaAPI:
    def __init__(self, phone):
        self.phone = phone
        self.base_url = "https://api.yollacalls.com"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "com.yollacalls/4.81 (Pixel 7; Android 15; en_IN)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Connection": "Keep-Alive"
        }
        self.device_id = "ccd1624fb6ad624bdd08e02086063486d6dd135b"
        self.android_id = "2c969a3eff46d674"

    def register(self, integrity_token=""):
        url = f"{self.base_url}/register"
        # Note: 'sign' is dynamic and would need to be calculated based on body content.
        # This script uses a static sign from the HAR for demonstration.
        payload = {
            "country": "IN",
            "device[hardware]": "panther",
            "device[app_version_code]": "5334",
            "device[model]": "Pixel 7",
            "sign": "B8F79851FFAC7D6D2266D09032E3A66B",
            "device[timezone]": "GMT+5",
            "language": "en",
            "device[language]": "en",
            "device[ad_id]": "f51ee336-e489-4882-8c21-95ff06ed4a9a",
            "device[rooted]": "false",
            "integrity_token": integrity_token,
            "device[product]": "panther",
            "device[android_id]": self.android_id,
            "phone": self.phone,
            "verify_by": "sms",
            "device[emulator_flags]": "telephony",
            "device[platform]": "android",
            "device[device_id]": self.device_id,
            "device[system_version]": "15",
            "device[emulator]": "false"
        }
        
        print(f"[*] Requesting OTP for {self.phone}...")
        response = requests.post(url, data=payload, headers=self.headers)
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response: {response.text}")
        return response.json()

    def verify(self, code):
        url = f"{self.base_url}/verify"
        payload = {
            "code": code,
            "device[android_id]": self.android_id,
            "phone": self.phone,
            "sign": "BCA4081F97FB057D35B79934279DEA17",
            "ad[device_advertising_id]": "f51ee336-e489-4882-8c21-95ff06ed4a9a",
            "device[timezone]": "GMT+5",
            "device[device_id]": self.device_id,
            "device[language]": "en",
            "device[ad_id]": "f51ee336-e489-4882-8c21-95ff06ed4a9a",
            "device[system_version]": "15",
            "device[rooted]": "false"
        }
        
        print(f"[*] Verifying code {code} for {self.phone}...")
        response = requests.post(url, data=payload, headers=self.headers)
        print(f"[+] Status: {response.status_code}")
        print(f"[+] Response: {response.text}")
        return response.json()

if __name__ == "__main__":
    # Example usage (will likely fail due to expired/invalid sign/token)
    api = YollaAPI("918791267460")
    # api.register("dummy_token")
    # api.verify("1234")
    print("Yolla API script loaded. Signature and Integrity Token required for live testing.")
