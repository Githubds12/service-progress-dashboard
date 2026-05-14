import requests
import json

class Liki24API:
    def __init__(self, phone_number):
        self.host = "https://api.liki24.it"
        self.phone_number = phone_number  # Format: "393471234567"
        self.session = requests.Session()
        self.common_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Liki24/2.2.13 (Android; 15; google_Pixel 7)",
            "X-Requested-With": "com.liki24.customerapp"
        }

    def register(self, firstname="Deepanshu", lastname="Singh", password="Password123!"):
        url = f"{self.host}/index.php?route=api/customer/registration/&smsHashCode=S0yl30QTVvt"
        payload = {
            "telephone": self.phone_number,
            "firstname": firstname,
            "lastname": lastname,
            "password": password
        }
        
        response = self.session.post(url, headers=self.common_headers, json=payload)
        return response.json()

    def verify_otp(self, otp_code):
        url = f"{self.host}/index.php?route=api/customer/verify/"
        payload = {
            "code": otp_code,
            "telephone": self.phone_number,
            "firebaseToken": ""
        }
        
        response = self.session.post(url, headers=self.common_headers, json=payload)
        try:
            return response.json()
        except:
            return response.text

if __name__ == "__main__":
    # Example Usage
    api = Liki24API("393471234567")
    
    print("Sending Registration Request...")
    # result = api.register()
    # print(json.dumps(result, indent=2))
    
    print("\nVerifying OTP...")
    # result = api.verify_otp("106145")
    # print(result)
