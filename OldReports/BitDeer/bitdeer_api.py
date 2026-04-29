import requests
import json
import time
import uuid

class BitdeerAPI:
    def __init__(self, phone_number):
        self.host = "https://galaxy.bitdeer.tech"
        self.phone_number = phone_number  # Format: "91-8791267460"
        self.session = requests.Session()
        self.common_headers = {
            "Content-Type": "application/json",
            "User-Agent": "Bitdeer/3.10.0 (Android; 15; google_Pixel 7)",
            "X-Android-Package": "com.bitdeer.cloud.android"
        }

    def get_common_data(self):
        return {
            "channel": "2",
            "device": "google_Pixel 7",
            "deviceip": "10.72.156.144",
            "language": "en_US",
            "nonce": uuid.uuid4().hex[:16],
            "platform": "android",
            "sdk": "15",
            "timestamp": str(int(time.time() * 1000)),
            "timezone": "GMT+05:30",
            "timezone_id": "Asia/Kolkata",
            "token": "bf8ac7b5-ffb8-4671-a206-9810ca2d4025",
            "version": "3.10.0"
        }

    def send_otp(self, geetest_data):
        """
        geetest_data should be a dict containing captcha_id, captcha_output, lot_number, etc.
        """
        url = f"{self.host}/api/user/passport/captcha"
        payload = {
            "identifier": self.phone_number,
            "license": "1409609154",
            "type": 1,
            "verify_data": geetest_data,
            "verify_lot": f"VL-{uuid.uuid4().hex}",
            "common": self.get_common_data()
        }
        
        response = self.session.post(url, headers=self.common_headers, json=payload)
        return response.json()

    def verify_otp(self, otp_code):
        url = f"{self.host}/api/user/passport/registerCheck"
        payload = {
            "captcha": otp_code,
            "identifier": self.phone_number,
            "type": 1,
            "common": self.get_common_data()
        }
        
        response = self.session.post(url, headers=self.common_headers, json=payload)
        return response.json()

if __name__ == "__main__":
    # Example Usage
    api = BitdeerAPI("91-8791267460")
    
    # Mocking GeeTest data (in reality, this comes from solving the challenge)
    mock_geetest = {
        "captcha_id": "adf6f520763439fd58ff8ba763e448be",
        "captcha_output": "MOCK_OUTPUT",
        "gen_time": str(int(time.time())),
        "lot_number": "MOCK_LOT",
        "pass_token": "MOCK_TOKEN"
    }
    
    print("Sending OTP Request...")
    # result = api.send_otp(mock_geetest)
    # print(json.dumps(result, indent=2))
    
    print("\nVerifying OTP...")
    # result = api.verify_otp("128735")
    # print(json.dumps(result, indent=2))
