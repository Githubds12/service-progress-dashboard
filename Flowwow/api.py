import requests

class FlowwowAPI:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://apis.flowwow.com"
        self.api2_url = "https://api2.flowwow.com"
        self.headers = {
            "User-Agent": "FW App android/5.3.2-PROD (com.flowwow; android:15; model:Pixel 7)",
            "FW-FB-TOKEN": "23024911",
            "Device-Unique-ID": "4a56fb123539e585",
            "adjust-device-id": "4f73900ad62db1507dd9b326054dfbe9",
            "Connection": "Keep-Alive",
        }

    def send_sms(self, phone, hash_val):
        """
        Send SMS OTP.
        Requires a valid hash calculated from parameters.
        """
        params = {
            "app_version": "5.3.2",
            "lang": "en",
            "partner_id": "1005",
            "phone": phone,
            "hash": hash_val
        }
        url = f"{self.base_url}/clientapp/client/smsCode"
        response = self.session.get(url, params=params, headers=self.headers)
        return response.json()

    def login(self, phone, code, hash_val):
        """
        Login with OTP code.
        Requires a valid hash.
        """
        params = {
            "app_version": "5.3.2",
            "lang": "en",
            "partner_id": "1005",
            "hash": hash_val
        }
        data = {
            "phone": phone,
            "code": code,
            "currency": "USD",
            "main_docs_agreed": "1",
            "advertising_agreed": "1"
        }
        url = f"{self.api2_url}/api2/client/login"
        response = self.session.post(url, params=params, data=data, headers=self.headers)
        return response.json()

if __name__ == "__main__":
    api = FlowwowAPI()
    
    # Test values from HAR
    test_phone = "393513820450"
    test_sms_hash = "28ab3c35e80c478a1956b8027b65ce3c"
    
    print("Testing Send SMS...")
    # This will likely fail or return success but won't send a new SMS if the hash/timestamp is old or tied to session
    res = api.send_sms(test_phone, test_sms_hash)
    print(res)
