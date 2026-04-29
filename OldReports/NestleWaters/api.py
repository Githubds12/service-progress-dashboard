import requests
import json

class NestleWatersAPI:
    def __init__(self, base_url="https://www.nestlewatersegypt.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 15; Pixel 7 Build/AP4A.250205.002)",
            "Host": "www.nestlewatersegypt.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

    def mobile_init(self):
        url = f"{self.base_url}/rest/en/V1/mobileinit"
        payload = {
            "customerlanguage": "en",
            "device_token": "",
            "device_type": "android",
            "lat": 0.0,
            "long": 0.0,
            "version": "2.0.69"
        }
        response = self.session.post(url, headers=self.headers, json=payload)
        return response.json()

    def send_otp(self, mobile, recaptcha_token):
        url = f"{self.base_url}/rest/en/V1/mobile/sendotp"
        payload = {
            "customer_mobile": mobile,
            "customer_mobile_code": mobile[:3], # Assuming first 3 are code, e.g., +91
            "device_type": "android",
            "lat": 0.0,
            "long": 0.0,
            "recaptchaToken": recaptcha_token
        }
        response = self.session.post(url, headers=self.headers, json=payload)
        return response.json()

    def verify_otp(self, mobile, otp):
        url = f"{self.base_url}/rest/en/V1/mobile/verifyotp"
        payload = {
            "customer_mobile": mobile,
            "email": " ",
            "lat": 0.0,
            "long": 0.0,
            "password": " ",
            "validation_code": otp
        }
        response = self.session.post(url, headers=self.headers, json=payload)
        return response.json()

if __name__ == "__main__":
    api = NestleWatersAPI()
    
    # Step 1: Init
    print("Initializing...")
    init_data = api.mobile_init()
    print(f"Init Status: {init_data.get('status')}")

    # Sample Mobile and Placeholder Recaptcha
    mobile = "+918791267460"
    sample_recaptcha = "0cAFcWeA..." # Needs real token
    
    # Step 2: Send OTP (Uncomment if you have a valid recaptcha token)
    # print(f"Sending OTP to {mobile}...")
    # send_res = api.send_otp(mobile, sample_recaptcha)
    # print(f"Send OTP Response: {send_res}")

    # Step 3: Verify OTP (Sample)
    otp = "188379"
    print(f"Verifying OTP {otp} for {mobile}...")
    verify_res = api.verify_otp(mobile, otp)
    print(f"Verify OTP Response: {verify_res}")
