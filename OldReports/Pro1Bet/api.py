import requests

class Pro1BetAPI:
    def __init__(self):
        self.base_url = "https://andind2022.com/Account"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "okhttp/4.12.0",
            "accept": "application/json"
        }

    def get_captcha(self, partner=315):
        url = f"{self.base_url}/v1/Mb/Register/GetRegCaptcha"
        params = {"partner": partner}
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()

    def register(self, phone, captcha_id, captcha_text):
        url = f"{self.base_url}/v1.1/Mb/Register/Registration"
        payload = {
            "CaptchaId": captcha_id,
            "ImageText": captcha_text,
            "Data": {
                "RegType": 2,
                "CountryId": 71,
                "CurrencyId": 99,
                "Phone": phone,
                "RulesConfirmation": 1,
                "SharePersonalDataConfirmation": 1,
                "TimeZone": "5.3"
            }
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def send_code(self, guid, token):
        url = f"{self.base_url}/v1/SendCode"
        payload = {
            "Data": {},
            "Auth": {
                "Guid": guid,
                "Token": token
            }
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def check_code(self, code, guid, token):
        url = f"{self.base_url}/v1/CheckCode"
        payload = {
            "Data": {
                "Code": code
            },
            "Auth": {
                "Guid": guid,
                "Token": token
            }
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

if __name__ == "__main__":
    api = Pro1BetAPI()
    phone = "6232975566"
    
    # Step 1: Get Captcha
    # print("[*] Fetching captcha...")
    # captcha = api.get_captcha()
    # print(captcha)
    
    # Step 2: Register (Requires solving the captcha)
    # print("[*] Registering...")
    # reg_res = api.register(phone, "f5d40a34-19d2-4b1a-bd6e-efc21a7eacbf", "SOLVED_CAPTCHA")
    # print(reg_res)
    
    # if reg_res.get("Success"):
    #     auth = reg_res["Value"]["Auth"]
    #     guid = auth["Guid"]
    #     token = auth["Token"]
        
    #     # Step 3: Send Code
    #     # print("[*] Sending OTP...")
    #     # send_res = api.send_code(guid, token)
    #     # print(send_res)
        
    #     # Step 4: Check Code
    #     # print("[*] Verifying OTP...")
    #     # check_res = api.check_code("123456", guid, token)
    #     # print(check_res)
