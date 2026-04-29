import requests
import json

class IBISmartAPI:
    def __init__(self):
        self.base_url = "https://smartapi.ibi.co.il/api"
        self.headers = {
            "api-key": "msdjfo@%#T^YrgsrfSFDHnmblpfsjbfsnk;ml358ueoj5%Y#Y%#yhfb#%@#$^T@4nt436hdgjmdhfmg",
            "User-Agent": "Android + 3.1.9",
            "Content-Type": "application/json; charset=UTF-8"
        }

    def request_otp(self, phone):
        url = f"{self.base_url}/onboarding/otp/start"
        payload = {"isVoice": False, "phone": phone}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def validate_otp(self, phone, code):
        url = f"{self.base_url}/onboarding/otp/validate"
        payload = {"code": code, "phone": phone, "utm_source": "app"}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

if __name__ == "__main__":
    api = IBISmartAPI()
    phone = "0541234567"
    
    print(f"Requesting OTP for {phone}...")
    res_start = api.request_otp(phone)
    print(f"Response: {json.dumps(res_start, indent=2)}")
    
    if res_start.get("success"):
        print("\nValidating OTP (sample code 123456)...")
        res_validate = api.validate_otp(phone, "123456")
        print(f"Response: {json.dumps(res_validate, indent=2)}")
