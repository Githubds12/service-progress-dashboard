import requests
import json

class DerivAPI:
    def __init__(self):
        self.base_url = "https://auth.deriv.com"
        self.headers = {
            "user-agent": "Dart/3.11 (dart:io)",
            "accept": "application/json",
            "content-type": "application/json"
        }
        self.session_token = None

    def get_registration_flow(self):
        url = f"{self.base_url}/self-service/registration/api"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_login_flow(self):
        url = f"{self.base_url}/self-service/login/api?refresh=true"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def request_phone_verification(self, flow_id, phone, session_token):
        url = f"{self.base_url}/self-service/login?flow={flow_id}"
        headers = self.headers.copy()
        headers["x-session-token"] = session_token
        payload = {
            "csrf_token": "",
            "method": "code",
            "identifier": phone,
            "transient_payload": {
                "action": "verify_phone",
                "lang": "en",
                "x-app": "com.deriv.home"
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def submit_otp(self, flow_id, phone, code, session_token):
        url = f"{self.base_url}/self-service/login?flow={flow_id}"
        headers = self.headers.copy()
        headers["x-session-token"] = session_token
        payload = {
            "csrf_token": "",
            "method": "code",
            "code": code,
            "identifier": phone,
            "transient_payload": {
                "lang": "en",
                "action": "verify_phone",
                "x-app": "com.deriv.home"
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

if __name__ == "__main__":
    api = DerivAPI()
    # Example usage:
    # flow = api.get_login_flow()
    # flow_id = flow['id']
    # api.request_phone_verification(flow_id, "+393516757384", "SESSION_TOKEN")
