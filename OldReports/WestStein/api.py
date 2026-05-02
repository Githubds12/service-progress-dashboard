import requests

class WestSteinAPI:
    def __init__(self, bearer_token=None):
        self.base_url = "https://api.weststeincard.com/api"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "okhttp/4.11.0",
            "X-Android-Package": "com.weststeincard.weststein",
            "accept": "application/json"
        }
        if bearer_token:
            self.headers["authorization"] = f"Bearer {bearer_token}"

    def apply_private(self, user_data, captcha_token):
        url = f"{self.base_url}/apply/private"
        payload = user_data.copy()
        payload["g-recaptcha-response"] = captcha_token
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json(), response.status_code

    def confirm_email(self, code):
        url = f"{self.base_url}/user/confirm/{code}"
        response = requests.post(url, headers=self.headers)
        return response.json(), response.status_code

    def request_phone_validation(self):
        url = f"{self.base_url}/user/phone/validate"
        response = requests.get(url, headers=self.headers)
        return response.json(), response.status_code

    def confirm_phone_validation(self, code):
        url = f"{self.base_url}/user/phone/confirm-validation"
        params = {
            "code": code,
            "language": "EN"
        }
        response = requests.post(url, params=params, headers=self.headers)
        return response.json(), response.status_code

if __name__ == "__main__":
    # Example usage (requires a valid JWT)
    api = WestSteinAPI(bearer_token="YOUR_JWT_HERE")
    
    # Step 1: Request Phone OTP
    # print("[*] Requesting phone validation...")
    # res, status = api.request_phone_validation()
    # print(f"Status: {status} | Res: {res}")
    
    # Step 2: Confirm Phone OTP
    # print("[*] Confirming phone validation...")
    # res, status = api.confirm_phone_validation("305398")
    # print(f"Status: {status} | Res: {res}")
