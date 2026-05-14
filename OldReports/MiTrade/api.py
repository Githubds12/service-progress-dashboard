import requests

class MiTradeAPI:
    def __init__(self, base_url="https://app.mokmoki.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 15; Pixel 7 Build/AP4A.250205.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.55 Mobile Safari/537.36",
            "Host": "app.mokmoki.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }

    def request_otp(self, phone, country_code, captcha_token, platform="google"):
        url = f"{self.base_url}/api/v1/misc/verification-codes"
        payload = {
            "phoneNumber": phone,
            "method": "SMS",
            "countryCallingCode": country_code,
            "purpose": "REGISTER",
            "reCAPTCHAToken": captcha_token,
            "reCAPTCHAPlatform": platform
        }
        response = self.session.post(url, headers=self.headers, data=payload)
        return response.json()

    def verify_otp(self, phone, country_code, code):
        url = f"{self.base_url}/api/v1/customers/verification/submit"
        payload = {
            "code": code,
            "countryCallingCode": country_code,
            "mobileNumber": phone,
            "type": "REGISTER"
        }
        response = self.session.post(url, headers=self.headers, data=payload)
        return response.json()

    def signup(self, phone, country_code, password, ticket):
        url = f"{self.base_url}/api/v1/customers/signup"
        payload = {
            "password": password,
            "baseCurrencyCode": "USD",
            "ticket": ticket,
            "countryCallingCode": country_code,
            "mobileNumber": phone,
            "registerCountryCode": "IN", # Assuming India based on +91
            "rememberMe": "true",
            "source": "app_android"
        }
        response = self.session.post(url, headers=self.headers, data=payload)
        return response.json()

if __name__ == "__main__":
    api = MiTradeAPI()
    
    # Placeholder data
    phone = "8791267460"
    country = "91"
    captcha = "[REAL_TOKEN]"
    
    # Step 1: Request OTP
    # print("Requesting OTP...")
    # res = api.request_otp(phone, country, captcha)
    # print(res)

    # Step 2: Verify OTP
    # print("Verifying OTP...")
    # res = api.verify_otp(phone, country, "449720")
    # print(res)
    # ticket = res.get("value", {}).get("ticket")

    # Step 3: Signup
    # if ticket:
    #     print("Completing Signup...")
    #     res = api.signup(phone, country, "YourPassword123", ticket)
    #     print(res)
