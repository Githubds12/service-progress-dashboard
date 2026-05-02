import requests
import json

class JamedaAPI:
    def __init__(self):
        self.base_url = "https://www.jameda.de/api/v3"
        self.token_url = "https://l.jameda.de/public/public-token"
        self.client_id = "10004_2hnb8qshsxgkcw48kgwk40ws4ogk8g8w800ss4s8wg0g04wwwo"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "okhttp/4.9.2",
            "app-version": "5.271.0",
            "platform-os": "android",
            "accept": "application/json"
        }

    def get_public_token(self):
        params = {"client_id": self.client_id}
        response = requests.get(self.token_url, params=params, headers={"User-Agent": "okhttp/4.9.2"})
        if response.status_code == 200:
            return response.json().get("token")
        return None

    def send_otp(self, phone, bearer_token):
        url = f"{self.base_url}/users/verification"
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {bearer_token}"
        payload = {
            "phone": phone,
            "context": "generic"
        }
        response = requests.put(url, json=payload, headers=headers)
        return response.json(), response.status_code

    def verify_otp(self, phone, code, email, captcha_token, bearer_token):
        url = f"{self.base_url}/users/verification"
        headers = self.headers.copy()
        headers["authorization"] = f"Bearer {bearer_token}"
        payload = {
            "code": code,
            "phone": phone,
            "email": email,
            "reCaptchaToken": captcha_token
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json(), response.status_code

if __name__ == "__main__":
    api = JamedaAPI()
    phone = "+393522296606"
    
    print("[*] Fetching public token...")
    bearer_token = api.get_public_token()
    if bearer_token:
        print(f"[+] Token: {bearer_token}")
        
        print(f"[*] Sending OTP to {phone}...")
        res, status = api.send_otp(phone, bearer_token)
        print(f"Status: {status}")
        print(f"Response: {res}")
        
        # Step 2 would require a real reCaptchaToken
        # print("[*] Verifying OTP...")
        # res, status = api.verify_otp(phone, "5976", "dkid8288@gmail.com", "YOUR_CAPTCHA_TOKEN", bearer_token)
        # print(f"Status: {status}")
        # print(f"Response: {res}")
    else:
        print("[-] Failed to fetch token")
