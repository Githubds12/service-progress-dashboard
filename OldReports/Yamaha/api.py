import requests

class YamahaAPI:
    def __init__(self):
        self.base_url = "https://www.c377768625-eu.com"
        self.api_key = "3_ebNf1cv6h3vwvGujn8ipy0Vwl4i0lW12fCe6WCdT39aZOr2Ab5wnpNLikFUPcjqf"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "okhttp/4.10.0"
        }

    def send_otp(self, phone, captcha_token):
        url = f"{self.base_url}/sendotp"
        payload = {
            "phoneNumber": phone,
            "locale": "en",
            "g-recaptcha-response": captcha_token,
            "apiKey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def verify_otp(self, phone, otp, token):
        url = f"{self.base_url}/authotp"
        payload = {
            "phoneNumber": phone,
            "otp": otp,
            "token": token,
            "apiKey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def register(self, phone, password, birth_data, token):
        url = f"{self.base_url}/register"
        payload = {
            "phoneNumber": phone,
            "password": password,
            "birthYear": birth_data.get("year"),
            "birthMonth": birth_data.get("month"),
            "birthDay": birth_data.get("day"),
            "token": token,
            "apiKey": self.api_key
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

if __name__ == "__main__":
    api = YamahaAPI()
    phone = "+918791267460"
    
    # Step 1: Send OTP (Requires Captcha)
    # print("Sending OTP...")
    # res = api.send_otp(phone, "[RECAPTCHA_TOKEN]")
    # print(res)
    # token = res.get("token")

    # Step 2: Verify OTP
    # if token:
    #     print("Verifying OTP...")
    #     res = api.verify_otp(phone, "610193", token)
    #     print(res)
    #     final_token = res.get("token")

    # Step 3: Register
    # if final_token:
    #     print("Registering...")
    #     birth = {"year": "1981", "month": "10", "day": "8"}
    #     res = api.register(phone, "YourPassword123", birth, final_token)
    #     print(res)
