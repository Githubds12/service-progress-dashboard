import requests
import uuid
import json

class OpenTableAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://mobile-api.opentable.com"
        self.token = None
        self.session_id = str(uuid.uuid4())
        self.headers = {
            "User-Agent": "com.opentable/26.13.2; android; android/15; 2.6/2400x1080; Anonymous",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8"
        }

    def get_anonymous_token(self):
        url = f"{self.base_url}/oauth/consumer/token"
        payload = "grant_type=implicit&client_id=ot-anonymous-apps&client_secret=0pentab1e"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": self.headers["User-Agent"]
        }
        try:
            response = self.session.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                self.session.headers.update({"Authorization": f"bearer {self.token}"})
                print(f"[+] Obtained Anonymous Token: {self.token}")
                return True
            print(f"[-] Failed to get token: {response.status_code}")
        except Exception as e:
            print(f"[-] Token Request Error: {e}")
        return False

    def start_2fa(self, country_code, country_id, phone_number):
        url = f"{self.base_url}/api/v1/2fa/start"
        payload = {
            "phone": {
                "countryCode": country_code,
                "countryId": country_id,
                "number": phone_number
            },
            "target": "SMS"
        }
        self.session.headers.update({"X-OT-SessionId": self.session_id})
        try:
            response = self.session.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                correlation_id = response.json().get("correlationId")
                print(f"[+] 2FA Started. Correlation ID: {correlation_id}")
                return correlation_id
            print(f"[-] 2FA Start Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[-] 2FA Start Error: {e}")
        return None

    def confirm_2fa(self, country_code, country_id, phone_number, code, correlation_id):
        url = f"{self.base_url}/api/v1/2fa/confirm"
        payload = {
            "allowPhoneRecycling": True,
            "code": code,
            "correlationId": correlation_id,
            "phone": {
                "countryCode": country_code,
                "countryId": country_id,
                "number": phone_number
            }
        }
        try:
            response = self.session.post(url, json=payload, headers=self.headers)
            if response.status_code == 200:
                print("[+] 2FA Confirmed Successfully!")
                return True
            print(f"[-] 2FA Confirm Failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[-] 2FA Confirm Error: {e}")
        return False

if __name__ == "__main__":
    api = OpenTableAPI()
    if api.get_anonymous_token():
        # Example test with a dummy number (Italy)
        corr_id = api.start_2fa("39", "IT", "3516308644")
        if corr_id:
            print("[*] Waiting for user to provide code...")
            # code = input("Enter OTP: ")
            # api.confirm_2fa("39", "IT", "3516308644", code, corr_id)
